from models.comment import Comment
from models.post import Post
from protocols.api_client_protocol import ApiClientProtocol


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
