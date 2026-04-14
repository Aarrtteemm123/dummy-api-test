from typing import Any, Protocol

import httpx


# PostService depends on this interface, not on DummyClient specifically (easier to test/swap).
class ApiClient(Protocol):
    async def get_post(self, post_id: int) -> dict[str, Any]: ...

    async def search_posts(self, query: str) -> list[dict[str, Any]]: ...

    async def get_comments(self, post_id: int) -> list[dict[str, Any]]: ...

    async def close(self) -> None: ...


class DummyClient:
    BASE_URL = "https://dummyjson.com"

    def __init__(self, timeout: float = 10.0):
        self._client = httpx.AsyncClient(base_url=self.BASE_URL, timeout=timeout)

    async def __aenter__(self) -> "DummyClient":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.close()

    async def get_post(self, post_id: int) -> dict[str, Any]:
        r = await self._client.get(f"/posts/{post_id}")
        r.raise_for_status()
        return r.json()

    async def search_posts(self, query: str) -> list[dict[str, Any]]:
        r = await self._client.get("/posts/search", params={"q": query})
        r.raise_for_status()
        # DummyJSON wraps results: { "posts": [...], "total", "skip", "limit" }.
        return r.json()["posts"]

    async def get_comments(self, post_id: int) -> list[dict[str, Any]]:
        r = await self._client.get(f"/posts/{post_id}/comments")
        r.raise_for_status()
        # Envelope: { "comments": [...], "total", "skip", "limit" }.
        return r.json()["comments"]

    async def close(self):
        await self._client.aclose()