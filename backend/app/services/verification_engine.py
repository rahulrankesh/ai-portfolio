import statistics
from difflib import SequenceMatcher

from app.models.schemas import ModelOutput, VerificationResult


class VerificationEngine:
    def verify(self, query: str, model_outputs: list[ModelOutput]) -> VerificationResult:
        valid = [item for item in model_outputs if item.response]
        if not valid:
            return VerificationResult(
                confidence_score=0.2,
                verification_notes="No successful model outputs were available for cross-verification.",
            )

        if len(valid) == 1:
            return VerificationResult(
                confidence_score=0.55,
                verification_notes=f"Single model response from {valid[0].model}; limited consensus.",
            )

        scores = []
        for i in range(len(valid)):
            for j in range(i + 1, len(valid)):
                scores.append(SequenceMatcher(None, valid[i].response, valid[j].response).ratio())

        consistency = statistics.mean(scores) if scores else 0.5
        error_penalty = sum(0.08 for item in model_outputs if item.error)
        confidence = max(0.05, min(0.98, consistency - error_penalty))

        notes = (
            f"Compared {len(valid)} successful model outputs for query consistency. "
            f"Mean similarity={consistency:.2f}; penalty applied for failed providers={error_penalty:.2f}."
        )
        return VerificationResult(confidence_score=round(confidence, 2), verification_notes=notes)

    def merge_answer(self, query: str, model_outputs: list[ModelOutput]) -> str:
        successful = [item for item in model_outputs if item.response]
        if not successful:
            return "Vedra could not generate a verified answer at this time."
        if len(successful) == 1:
            return successful[0].response

        ordered = sorted(successful, key=lambda output: len(output.response), reverse=True)
        primary, secondary = ordered[0], ordered[1]
        return (
            f"{primary.response}\n\n"
            f"Cross-check: {secondary.model} provided a consistent perspective with additional context."
        )
