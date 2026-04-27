from types import TracebackType
from typing import Any

import httpx


class DummyClient:
    base_url = "https://dummyjson.com"

    def __init__(
        self,
        timeout: float = 10.0,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        if transport is None:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=timeout,
            )
        else:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=timeout,
                transport=transport,
            )

    async def __aenter__(self) -> "DummyClient":
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        await self.close()

    async def get_post(self, post_id: int) -> dict[str, Any]:
        response = await self._client.get(f"/posts/{post_id}")
        response.raise_for_status()
        return response.json()

    async def search_posts(self, query: str) -> list[dict[str, Any]]:
        response = await self._client.get("/posts/search", params={"q": query})
        response.raise_for_status()
        return response.json()["posts"]

    async def get_comments(self, post_id: int) -> list[dict[str, Any]]:
        response = await self._client.get(f"/posts/{post_id}/comments")
        response.raise_for_status()
        return response.json()["comments"]

    async def close(self) -> None:
        await self._client.aclose()
