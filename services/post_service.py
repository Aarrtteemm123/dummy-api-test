from collections.abc import Sequence

from models.comment import Comment
from models.post import Post
from protocols.api_client_protocol import ApiClientProtocol
from protocols.storage_protocol import StorageProtocol


class PostLoaderService:
    """Loads posts and comments from the API and maps them to models."""

    def __init__(self, client: ApiClientProtocol) -> None:
        self._client = client

    async def fetch_post(self, post_id: int) -> Post:
        """Load one post from the API and map it to :class:`Post`."""
        raw = await self._client.get_post(post_id)
        return Post.from_data(raw)

    async def fetch_posts_by_query(self, query: str) -> list[Post]:
        """Search the API and return models."""
        raw_posts = await self._client.search_posts(query)
        return [Post.from_data(raw) for raw in raw_posts]

    async def fetch_comments(self, post_id: int) -> list[Comment]:
        """Load comments for a post from the API."""
        raw_comments = await self._client.get_comments(post_id)
        return [Comment.from_data(raw) for raw in raw_comments]


class PostStorageService:
    """Persists Post and Comment models into a storage backend."""

    posts_collection = "posts"
    comments_collection = "comments"

    def __init__(self, storage: StorageProtocol) -> None:
        self._storage = storage

    def save_post(self, post: Post, storage_key: int) -> None:
        """Store a post under a given key."""
        self._storage.create(PostStorageService.posts_collection, storage_key, post)

    def save_posts(self, posts: Sequence[Post]) -> None:
        """Persist many posts, keyed by each :attr:`Post.id`."""
        self._put_by_entity_id(PostStorageService.posts_collection, list(posts))

    def save_comments(self, comments: Sequence[Comment]) -> None:
        """Persist many comments, keyed by each :attr:`Comment.id`."""
        self._put_by_entity_id(PostStorageService.comments_collection, list(comments))

    def _put_by_entity_id(self, collection: str, items: list[Post] | list[Comment]) -> None:
        if not items:
            return
        pairs = [(item.id, item) for item in items]
        self._storage.create_many(collection, pairs)
