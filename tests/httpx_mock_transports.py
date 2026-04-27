from functools import partial
from typing import Any

import httpx

from tests.httpx_responders import (
    respond_comments,
    respond_get_post,
    respond_not_found,
    respond_search_love,
)


def transport_get_post(
    path_suffix: str,
    body: dict[str, Any],
) -> httpx.MockTransport:
    return httpx.MockTransport(
        partial(
            respond_get_post,
            path_suffix=path_suffix,
            body=body,
        ),
    )


def transport_search_love(
    posts: list[dict[str, Any]],
) -> httpx.MockTransport:
    return httpx.MockTransport(
        partial(respond_search_love, posts=posts),
    )


def transport_comments(
    comments: list[dict[str, Any]],
) -> httpx.MockTransport:
    return httpx.MockTransport(
        partial(respond_comments, comments=comments),
    )


def transport_not_found() -> httpx.MockTransport:
    return httpx.MockTransport(respond_not_found)
