from typing import Any

import httpx


class DummyClient:
    base_url = "https://dummyjson.com"

    def __init__(
        self,
        timeout: float = 10.0,
        transport: httpx.BaseTransport | None = None,
    ):
        client_config: dict[str, object] = {
            "base_url": self.base_url,
            "timeout": timeout,
        }
        if transport is not None:
            client_config["transport"] = transport
        self._client = httpx.AsyncClient(**client_config)

    async def __aenter__(self) -> "DummyClient":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.close()

    async def get_post(self, post_id: int) -> dict[str, Any]:
        response = await self._client.get(f"/posts/{post_id}")
        response.raise_for_status()
        return response.json()

    async def search_posts(self, query: str) -> list[dict[str, Any]]:
        response = await self._client.get("/posts/search", params={"q": query})
        response.raise_for_status()
        # DummyJSON wraps results: { "posts": [...], "total", "skip", "limit" }.
        return response.json()["posts"]

    async def get_comments(self, post_id: int) -> list[dict[str, Any]]:
        response = await self._client.get(f"/posts/{post_id}/comments")
        response.raise_for_status()
        # Envelope: { "comments": [...], "total", "skip", "limit" }.
        return response.json()["comments"]

    async def close(self):
        await self._client.aclose()