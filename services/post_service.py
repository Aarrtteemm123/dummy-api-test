from dataclasses import asdict

from clients.dummy_client import ApiClient
from models.comment import Comment
from models.post import Post
from storage import Storage


class PostService:
    POSTS = "posts"
    COMMENTS = "comments"

    def __init__(self, client: ApiClient, storage: Storage) -> None:
        self._client = client
        self._storage = storage

    async def fetch_and_store_post(self, post_id: int) -> Post:
        raw = await self._client.get_post(post_id)
        post = Post.from_data(raw)
        self._storage.create(PostService.POSTS, post_id, asdict(post))
        return post

    async def search_and_store_posts(self, query: str) -> list[Post]:
        raw_posts = await self._client.search_posts(query)
        result: list[Post] = []
        for raw in raw_posts:
            post = Post.from_data(raw)
            self._storage.create(PostService.POSTS, post.id, asdict(post))
            result.append(post)
        return result

    async def fetch_and_store_comments(self, post_id: int) -> list[Comment]:
        raw_comments = await self._client.get_comments(post_id)
        result: list[Comment] = []
        for raw in raw_comments:
            comment = Comment.from_data(raw)
            self._storage.create(PostService.COMMENTS, comment.id, asdict(comment))
            result.append(comment)
        return result