from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    query: str = Field(min_length=2, max_length=2000)
    language: str = Field(default="en")
    privacy_mode: bool = False


class ModelOutput(BaseModel):
    model: str
    response: str
    latency_ms: int | None = None
    error: str | None = None


class VideoItem(BaseModel):
    title: str
    url: str
    views: int
    published_at: datetime
    thumbnail: str
    quality: str = "HD"


class ImageItem(BaseModel):
    url: str
    source: str
    resolution: str = "HD"


class VerificationResult(BaseModel):
    confidence_score: float = Field(ge=0, le=1)
    verification_notes: str


class QueryResponse(BaseModel):
    query: str
    final_answer: str
    model_outputs: list[ModelOutput]
    confidence_score: float
    verification_notes: str
    sources: list[dict[str, Any]]
    videos: list[VideoItem]
    images: list[ImageItem]
