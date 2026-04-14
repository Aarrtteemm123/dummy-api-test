from unittest.mock import AsyncMock

import pytest

from models.comment import Comment, CommentUser
from models.post import Post
from services.post_service import PostService
from storage import InMemoryStorage


@pytest.fixture
def storage() -> InMemoryStorage:
    return InMemoryStorage()


@pytest.fixture
def client() -> AsyncMock:
    return AsyncMock()


@pytest.mark.asyncio
async def test_fetch_and_store_post_uses_request_id_as_key(
    client: AsyncMock,
    storage: InMemoryStorage,
) -> None:
    client.get_post = AsyncMock(
        return_value={
            "id": 999,
            "title": "t",
            "body": "b",
            "tags": [],
            "userId": 1,
        }
    )
    service = PostService(client, storage)
    post = await service.fetch_and_store_post(post_id=1)

    assert isinstance(post, Post)
    assert post.id == 999
    stored = storage.read(PostService.POSTS, 1)
    assert stored is post
    client.get_post.assert_awaited_once_with(1)


@pytest.mark.asyncio
async def test_search_and_store_posts(
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
        ]
    )
    service = PostService(client, storage)
    posts = await service.search_and_store_posts("love")

    assert len(posts) == 2
    assert storage.read(PostService.POSTS, 2) is posts[0]
    assert storage.read(PostService.POSTS, 3) is posts[1]
    client.search_posts.assert_awaited_once_with("love")


@pytest.mark.asyncio
async def test_fetch_and_store_comments(
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
        ]
    )
    service = PostService(client, storage)
    comments = await service.fetch_and_store_comments(2)

    assert len(comments) == 1
    assert isinstance(comments[0], Comment)
    assert comments[0].user == CommentUser(id=1, username="a", fullName="A")
    assert storage.read(PostService.COMMENTS, 100) is comments[0]
    client.get_comments.assert_awaited_once_with(2)
