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
        self._storage.create(PostService.POSTS, post_id, post)
        return post

    async def search_and_store_posts(self, query: str) -> list[Post]:
        raw_posts = await self._client.search_posts(query)
        posts: list[Post] = []
        pairs: list[tuple[int, Post]] = []
        for raw in raw_posts:
            p = Post.from_data(raw)
            posts.append(p)
            pairs.append((p.id, p))
        self._storage.create_many(PostService.POSTS, pairs)
        return posts

    async def fetch_and_store_comments(self, post_id: int) -> list[Comment]:
        raw_comments = await self._client.get_comments(post_id)
        comments: list[Comment] = []
        pairs: list[tuple[int, Comment]] = []
        for raw in raw_comments:
            c = Comment.from_data(raw)
            comments.append(c)
            pairs.append((c.id, c))
        self._storage.create_many(PostService.COMMENTS, pairs)
        return comments