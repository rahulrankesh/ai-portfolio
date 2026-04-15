import asyncio

from fastapi import APIRouter, Depends

from app.core.cache import CacheClient
from app.core.config import Settings, get_settings
from app.models.schemas import ImageItem, QueryRequest, QueryResponse, VideoItem
from app.services.ai_orchestrator import AIOrchestrator
from app.services.image_service import ImageService
from app.services.verification_engine import VerificationEngine
from app.services.youtube_service import YouTubeService

router = APIRouter()


def get_cache(settings: Settings = Depends(get_settings)) -> CacheClient:
    return CacheClient(settings)


@router.post("/videos", response_model=dict[str, list[VideoItem]])
async def videos_endpoint(request: QueryRequest, settings: Settings = Depends(get_settings)):
    videos = await YouTubeService(settings).search(request.query)
    return {"videos": videos}


@router.post("/images", response_model=dict[str, list[ImageItem]])
async def images_endpoint(request: QueryRequest, settings: Settings = Depends(get_settings)):
    images = await ImageService(settings).search(request.query)
    return {"images": images}


@router.post("/query", response_model=QueryResponse)
async def query_endpoint(
    request: QueryRequest,
    settings: Settings = Depends(get_settings),
    cache: CacheClient = Depends(get_cache),
):
    cache_payload = {"query": request.query, "language": request.language}
    if not request.privacy_mode:
        cached = await cache.get_json("query", cache_payload)
        if cached:
            return QueryResponse(**cached)

    ai_orchestrator = AIOrchestrator(settings)
    verification_engine = VerificationEngine()
    youtube_service = YouTubeService(settings)
    image_service = ImageService(settings)

    model_outputs, videos, images = await asyncio.gather(
        ai_orchestrator.run_parallel(request.query),
        youtube_service.search(request.query),
        image_service.search(request.query),
    )

    verification = verification_engine.verify(request.query, model_outputs)
    final_answer = verification_engine.merge_answer(request.query, model_outputs)
    response = QueryResponse(
        query=request.query,
        final_answer=final_answer,
        model_outputs=model_outputs,
        confidence_score=verification.confidence_score,
        verification_notes=verification.verification_notes,
        sources=[
            {"type": "youtube", "count": len(videos)},
            {"type": "images", "count": len(images)},
        ],
        videos=videos,
        images=images,
    )

    if not request.privacy_mode:
        await cache.set_json("query", cache_payload, response.model_dump(mode="json"))

    return response
