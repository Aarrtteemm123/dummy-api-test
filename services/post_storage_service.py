from collections.abc import Sequence

from models.comment import Comment
from models.post import Post
from protocols.storage_protocol import StorageProtocol


class PostStorageService:
    """Persists Post and Comment models into a storage backend."""

    posts_collection = "posts"
    comments_collection = "comments"

    def __init__(self, storage: StorageProtocol) -> None:
        self._storage = storage

    def save_post(self, post: Post, storage_key: int) -> None:
        self._storage.create(
            PostStorageService.posts_collection,
            storage_key,
            post,
        )

    def save_posts(self, posts: Sequence[Post]) -> None:
        self._put_by_entity_id(
            PostStorageService.posts_collection,
            list(posts),
        )

    def save_comments(self, comments: Sequence[Comment]) -> None:
        self._put_by_entity_id(
            PostStorageService.comments_collection,
            list(comments),
        )

    def _put_by_entity_id(
        self,
        collection: str,
        entity_list: list[Post] | list[Comment],
    ) -> None:
        if not entity_list:
            return
        pairs = [(entity.id, entity) for entity in entity_list]
        self._storage.create_many(collection, pairs)
