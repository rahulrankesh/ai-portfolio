import asyncio
import time
from dataclasses import dataclass

import httpx

from app.core.config import Settings
from app.models.schemas import ModelOutput


@dataclass
class AIModelClient:
    name: str

    async def generate(self, query: str) -> ModelOutput:
        raise NotImplementedError


class OpenAIClient(AIModelClient):
    def __init__(self, settings: Settings):
        super().__init__(name="openai")
        self._api_key = settings.openai_api_key
        self._timeout = settings.default_model_timeout_seconds

    async def generate(self, query: str) -> ModelOutput:
        if not self._api_key:
            return ModelOutput(model=self.name, response="", error="OPENAI_API_KEY missing")

        started = time.perf_counter()
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            resp = await client.post(
                "https://api.openai.com/v1/responses",
                headers={"Authorization": f"Bearer {self._api_key}"},
                json={"model": "gpt-4.1-mini", "input": query},
            )
            resp.raise_for_status()
            data = resp.json()

        output_text = data.get("output_text") or ""
        if not output_text and data.get("output"):
            parts = []
            for item in data["output"]:
                for content in item.get("content", []):
                    if content.get("type") == "output_text":
                        parts.append(content.get("text", ""))
            output_text = "\n".join(parts)

        return ModelOutput(
            model=self.name,
            response=output_text.strip(),
            latency_ms=int((time.perf_counter() - started) * 1000),
        )


class AnthropicClient(AIModelClient):
    def __init__(self, settings: Settings):
        super().__init__(name="anthropic")
        self._api_key = settings.anthropic_api_key
        self._timeout = settings.default_model_timeout_seconds

    async def generate(self, query: str) -> ModelOutput:
        if not self._api_key:
            return ModelOutput(model=self.name, response="", error="ANTHROPIC_API_KEY missing")

        started = time.perf_counter()
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            resp = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": self._api_key,
                    "anthropic-version": "2023-06-01",
                },
                json={
                    "model": "claude-3-5-sonnet-latest",
                    "max_tokens": 500,
                    "messages": [{"role": "user", "content": query}],
                },
            )
            resp.raise_for_status()
            data = resp.json()

        text_parts = [item.get("text", "") for item in data.get("content", []) if item.get("type") == "text"]
        return ModelOutput(
            model=self.name,
            response="\n".join(text_parts).strip(),
            latency_ms=int((time.perf_counter() - started) * 1000),
        )


class FallbackHeuristicClient(AIModelClient):
    def __init__(self):
        super().__init__(name="heuristic")

    async def generate(self, query: str) -> ModelOutput:
        return ModelOutput(model=self.name, response=f"No cloud model available. Received query: {query}")


class AIOrchestrator:
    def __init__(self, settings: Settings):
        self._clients: list[AIModelClient] = [OpenAIClient(settings), AnthropicClient(settings)]

    async def run_parallel(self, query: str) -> list[ModelOutput]:
        tasks = [client.generate(query) for client in self._clients]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        outputs: list[ModelOutput] = []
        for idx, result in enumerate(results):
            if isinstance(result, Exception):
                outputs.append(
                    ModelOutput(
                        model=self._clients[idx].name,
                        response="",
                        error=f"{type(result).__name__}: {result}",
                    )
                )
            else:
                outputs.append(result)

        if all(not item.response for item in outputs):
            outputs.append(await FallbackHeuristicClient().generate(query))

        return outputs
