from dummyjson_client import DummyClient
from storage import InMemoryStorage


class PostService:
    def __init__(self, client: DummyClient, storage: InMemoryStorage):
        self.client = client
        self.storage = storage

    async def fetch_and_store_post(self, post_id: int) -> dict:
        post = await self.client.get_post(post_id)
        self.storage.create("posts", post_id, post)
        return post

    async def search_and_store_posts(self, query: str) -> list:
        posts = await self.client.search_posts(query)
        for post in posts:
            self.storage.create("posts", post["id"], post)
        return posts

    async def fetch_and_store_comments(self, post_id: int) -> list:
        comments = await self.client.get_comments(post_id)
        for comment in comments:
            self.storage.create("comments", comment["id"], comment)
        return comments