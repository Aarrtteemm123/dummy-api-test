from unittest.mock import AsyncMock

import pytest

from models.comment import Comment, CommentUser
from models.post import Post
from services.post_service import PostLoaderService, PostStorageService
from storage import InMemoryStorage

BODY_ID_MISMATCH = 999


@pytest.fixture
def storage() -> InMemoryStorage:
    return InMemoryStorage()


@pytest.fixture
def client() -> AsyncMock:
    return AsyncMock()


@pytest.mark.asyncio
async def test_loader_fetch_post_does_not_write_to_storage(
    client: AsyncMock,
    storage: InMemoryStorage,
) -> None:
    client.get_post = AsyncMock(
        return_value={
            "id": 1,
            "title": "t",
            "body": "b",
            "tags": [],
            "userId": 1,
        },
    )
    loader = PostLoaderService(client)
    await loader.fetch_post(1)
    assert storage.read(PostStorageService.posts_collection, 1) is None


@pytest.mark.asyncio
async def test_save_post_uses_storage_key(
    client: AsyncMock,
    storage: InMemoryStorage,
) -> None:
    client.get_post = AsyncMock(
        return_value={
            "id": BODY_ID_MISMATCH,
            "title": "t",
            "body": "b",
            "tags": [],
            "userId": 1,
        },
    )
    loader = PostLoaderService(client)
    post_storage = PostStorageService(storage)
    post = await loader.fetch_post(1)
    post_storage.save_post(post, storage_key=1)

    assert isinstance(post, Post)
    assert post.id == BODY_ID_MISMATCH
    assert storage.read(PostStorageService.posts_collection, 1) is post
    client.get_post.assert_awaited_once_with(1)


@pytest.mark.asyncio
async def test_query_posts_then_persist(
    client: AsyncMock,
    storage: InMemoryStorage,
) -> None:
    client.search_posts = AsyncMock(
        return_value=[
            {
                "id": 2,
                "title": "a",
                "body": "b",
                "tags": [],
                "userId": 1,
            },
            {
                "id": 3,
                "title": "c",
                "body": "d",
                "tags": ["t"],
                "userId": 2,
            },
        ],
    )
    loader = PostLoaderService(client)
    post_storage = PostStorageService(storage)
    posts = await loader.fetch_posts_by_query("love")
    post_storage.save_posts(posts)

    assert len(posts) == 2
    assert storage.read(PostStorageService.posts_collection, 2) is posts[0]
    assert storage.read(PostStorageService.posts_collection, 3) is posts[1]
    client.search_posts.assert_awaited_once_with("love")


@pytest.mark.asyncio
async def test_fetch_comments_then_persist(
    client: AsyncMock,
    storage: InMemoryStorage,
) -> None:
    client.get_comments = AsyncMock(
        return_value=[
            {
                "id": 100,
                "body": "c1",
                "postId": 2,
                "likes": 1,
                "user": {"id": 1, "username": "a", "fullName": "A"},
            },
        ],
    )
    loader = PostLoaderService(client)
    post_storage = PostStorageService(storage)
    comments = await loader.fetch_comments(2)
    post_storage.save_comments(comments)

    assert len(comments) == 1
    assert isinstance(comments[0], Comment)
    assert comments[0].user == CommentUser(id=1, username="a", fullname="A")
    assert storage.read(PostStorageService.comments_collection, 100) is comments[0]
    client.get_comments.assert_awaited_once_with(2)
