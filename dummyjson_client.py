import httpx


class DummyClient:
    BASE_URL = "https://dummyjson.com"

    def __init__(self, timeout=10.0):
        self._client = httpx.AsyncClient(base_url=self.BASE_URL, timeout=timeout)

    async def get_post(self, post_id: int) -> dict:
        r = await self._client.get(f"/posts/{post_id}")
        r.raise_for_status()
        return r.json()

    async def search_posts(self, query: str) -> list:
        r = await self._client.get("/posts/search", params={"q": query})
        r.raise_for_status()
        return r.json()["posts"]

    async def get_comments(self, post_id: int) -> list:
        r = await self._client.get(f"/posts/{post_id}/comments")
        r.raise_for_status()
        return r.json()["comments"]

    async def close(self):
        await self._client.aclose()