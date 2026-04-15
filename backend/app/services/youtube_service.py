from datetime import datetime, timezone

import httpx

from app.core.config import Settings
from app.models.schemas import VideoItem


class YouTubeService:
    def __init__(self, settings: Settings):
        self._api_key = settings.youtube_api_key

    async def search(self, query: str, max_results: int = 8) -> list[VideoItem]:
        if not self._api_key:
            return []

        async with httpx.AsyncClient(timeout=20) as client:
            search_resp = await client.get(
                "https://www.googleapis.com/youtube/v3/search",
                params={
                    "key": self._api_key,
                    "part": "snippet",
                    "q": query,
                    "type": "video",
                    "videoDefinition": "high",
                    "maxResults": max_results,
                    "order": "relevance",
                },
            )
            search_resp.raise_for_status()
            items = search_resp.json().get("items", [])

            video_ids = [item["id"]["videoId"] for item in items if item.get("id", {}).get("videoId")]
            if not video_ids:
                return []

            details_resp = await client.get(
                "https://www.googleapis.com/youtube/v3/videos",
                params={
                    "key": self._api_key,
                    "part": "snippet,statistics,contentDetails",
                    "id": ",".join(video_ids),
                },
            )
            details_resp.raise_for_status()
            details = details_resp.json().get("items", [])

        videos: list[VideoItem] = []
        for item in details:
            snippet = item.get("snippet", {})
            thumbnails = snippet.get("thumbnails", {})
            if "high" not in thumbnails:
                continue

            video = VideoItem(
                title=snippet.get("title", "Untitled"),
                url=f"https://www.youtube.com/watch?v={item['id']}",
                views=int(item.get("statistics", {}).get("viewCount", 0)),
                published_at=datetime.fromisoformat(snippet.get("publishedAt", "1970-01-01T00:00:00Z").replace("Z", "+00:00")),
                thumbnail=thumbnails["high"].get("url", ""),
                quality="HD",
            )
            videos.append(video)

        return self._sort_videos(videos)

    @staticmethod
    def _sort_videos(videos: list[VideoItem]) -> list[VideoItem]:
        now = datetime.now(timezone.utc)

        def recency_weight(item: VideoItem) -> float:
            age_days = max(1, (now - item.published_at).days)
            return 1 / age_days

        return sorted(videos, key=lambda item: (item.views, recency_weight(item), item.published_at.timestamp()), reverse=True)
