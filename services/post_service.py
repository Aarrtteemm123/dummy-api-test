from typing import Any

from clients.dummy_client import ApiClient
from storage import Storage

POSTS = "posts"
COMMENTS = "comments"


class PostService:
    def __init__(self, client: ApiClient, storage: Storage) -> None:
        self._client = client
        self._storage = storage

    async def fetch_and_store_post(self, post_id: int) -> dict[str, Any]:
        post = await self._client.get_post(post_id)
        self._storage.create(POSTS, post_id, post)
        return post

    async def search_and_store_posts(self, query: str) -> list[dict[str, Any]]:
        posts = await self._client.search_posts(query)
        for post in posts:
            self._storage.create(POSTS, post["id"], post)
        return posts

    async def fetch_and_store_comments(self, post_id: int) -> list[dict[str, Any]]:
        comments = await self._client.get_comments(post_id)
        for comment in comments:
            self._storage.create(COMMENTS, comment["id"], comment)
        return comments