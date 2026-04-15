from urllib.parse import urlparse

import httpx

from app.core.config import Settings
from app.models.schemas import ImageItem


class ImageService:
    def __init__(self, settings: Settings):
        self._unsplash_key = settings.unsplash_api_key
        self._google_key = settings.google_cse_api_key
        self._google_cse_id = settings.google_cse_id

    async def search(self, query: str, max_results: int = 12) -> list[ImageItem]:
        unsplash_items = await self._search_unsplash(query, max_results=max_results)
        if unsplash_items:
            return self._dedupe(unsplash_items)
        google_items = await self._search_google_cse(query, max_results=max_results)
        return self._dedupe(google_items)

    async def _search_unsplash(self, query: str, max_results: int) -> list[ImageItem]:
        if not self._unsplash_key:
            return []

        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.get(
                "https://api.unsplash.com/search/photos",
                params={"query": query, "per_page": max_results, "orientation": "landscape"},
                headers={"Authorization": f"Client-ID {self._unsplash_key}"},
            )
            resp.raise_for_status()
            data = resp.json()

        images = []
        for item in data.get("results", []):
            if item.get("width", 0) < 1280 or item.get("height", 0) < 720:
                continue
            images.append(
                ImageItem(
                    url=item.get("urls", {}).get("regular", ""),
                    source=item.get("links", {}).get("html", "unsplash"),
                    resolution="HD",
                )
            )
        return images

    async def _search_google_cse(self, query: str, max_results: int) -> list[ImageItem]:
        if not self._google_key or not self._google_cse_id:
            return []

        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.get(
                "https://customsearch.googleapis.com/customsearch/v1",
                params={
                    "key": self._google_key,
                    "cx": self._google_cse_id,
                    "q": query,
                    "searchType": "image",
                    "imgSize": "xlarge",
                    "num": min(max_results, 10),
                    "safe": "active",
                },
            )
            resp.raise_for_status()
            data = resp.json()

        images = []
        for item in data.get("items", []):
            images.append(
                ImageItem(
                    url=item.get("link", ""),
                    source=item.get("displayLink", "google"),
                    resolution="HD",
                )
            )
        return images

    @staticmethod
    def _dedupe(images: list[ImageItem]) -> list[ImageItem]:
        unique: dict[str, ImageItem] = {}
        for image in images:
            key = urlparse(image.url).path
            if key and key not in unique:
                unique[key] = image
        return list(unique.values())
