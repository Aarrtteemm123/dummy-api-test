import json

import httpx
import pytest

from clients.dummy_client import DummyClient


def _json_response(payload: object, status: int = 200) -> httpx.Response:
    return httpx.Response(
        status,
        content=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
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

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert str(request.url).endswith("/posts/1")
        return _json_response(body)

    transport = httpx.MockTransport(handler)
    async with DummyClient(transport=transport) as client:
        assert await client.get_post(1) == body


@pytest.mark.asyncio
async def test_search_posts_unwraps_envelope() -> None:
    posts = [{"id": 1, "title": "x", "body": "y", "tags": [], "userId": 1}]

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.params["q"] == "love"
        return _json_response({"posts": posts, "total": 1, "skip": 0, "limit": 10})

    transport = httpx.MockTransport(handler)
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
        }
    ]

    def handler(request: httpx.Request) -> httpx.Response:
        assert "/posts/2/comments" in str(request.url)
        return _json_response(
            {"comments": comments, "total": 1, "skip": 0, "limit": 10}
        )

    transport = httpx.MockTransport(handler)
    async with DummyClient(transport=transport) as client:
        assert await client.get_comments(2) == comments


@pytest.mark.asyncio
async def test_http_error_raises() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(404, text="not found")

    transport = httpx.MockTransport(handler)
    async with DummyClient(transport=transport) as client:
        with pytest.raises(httpx.HTTPStatusError):
            await client.get_post(99)
