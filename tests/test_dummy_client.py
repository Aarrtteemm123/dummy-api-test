import httpx
import pytest

from clients.dummy_client import DummyClient
from tests.http_constants import UNKNOWN_POST_ID
from tests.httpx_mock_transports import (
    transport_comments,
    transport_get_post,
    transport_not_found,
    transport_search_love,
)


@pytest.mark.asyncio
async def test_get_post_parses_json() -> None:
    body = {
        "id": 1,
        "title": "t",
        "body": "b",
        "tags": [],
        "userId": 5,
    }
    transport = transport_get_post("/posts/1", body)
    async with DummyClient(transport=transport) as client:
        assert await client.get_post(1) == body


@pytest.mark.asyncio
async def test_search_posts_unwraps_envelope() -> None:
    posts = [{"id": 1, "title": "x", "body": "y", "tags": [], "userId": 1}]
    transport = transport_search_love(posts)
    async with DummyClient(transport=transport) as client:
        assert await client.search_posts("love") == posts


@pytest.mark.asyncio
async def test_get_comments_unwraps_envelope() -> None:
    comments = [
        {
            "id": 1,
            "body": "b",
            "postId": 2,
            "likes": 0,
            "user": {"id": 1, "username": "u", "fullName": ""},
        },
    ]
    transport = transport_comments(comments)
    async with DummyClient(transport=transport) as client:
        assert await client.get_comments(2) == comments


@pytest.mark.asyncio
async def test_http_error_raises() -> None:
    async with DummyClient(transport=transport_not_found()) as client:
        with pytest.raises(httpx.HTTPStatusError):
            await client.get_post(UNKNOWN_POST_ID)
