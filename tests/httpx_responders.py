import json
from typing import Any

import httpx

from tests.http_constants import HTTP_STATUS_NOT_FOUND


def json_for_tests(payload: object, status: int = 200) -> httpx.Response:
    return httpx.Response(
        status,
        content=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )


def respond_get_post(
    request: httpx.Request,
    *,
    path_suffix: str,
    body: dict[str, Any],
) -> httpx.Response:
    assert request.method == "GET"
    assert str(request.url).endswith(path_suffix)
    return json_for_tests(body)


def respond_search_love(
    request: httpx.Request,
    *,
    posts: list[dict[str, Any]],
) -> httpx.Response:
    assert request.url.params["q"] == "love"
    return json_for_tests(
        {"posts": posts, "total": 1, "skip": 0, "limit": 10},
    )


def respond_comments(
    request: httpx.Request,
    *,
    comments: list[dict[str, Any]],
) -> httpx.Response:
    assert "/posts/2/comments" in str(request.url)
    return json_for_tests(
        {"comments": comments, "total": 1, "skip": 0, "limit": 10},
    )


def respond_not_found(_request: httpx.Request) -> httpx.Response:
    return httpx.Response(HTTP_STATUS_NOT_FOUND, text="not found")
