import asyncio
import sys

import httpx

from clients.dummy_client import DummyClient
from services.post_service import PostService
from storage import InMemoryStorage


async def main() -> None:
    try:
        async with DummyClient() as client:
            storage = InMemoryStorage()
            service = PostService(client, storage)

            await service.fetch_and_store_post(1)
            await service.search_and_store_posts("love")
            await service.fetch_and_store_comments(2)
            print("Stored posts:", storage.list_collection("posts"))
            print("Stored comments:", storage.list_collection("comments"))
    except httpx.HTTPStatusError as exc:
        print(
            f"HTTP {exc.response.status_code} for {exc.request.url!r}",
            file=sys.stderr,
        )
    except httpx.RequestError as exc:
        print(f"RequestError: {exc}", file=sys.stderr)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)


if __name__ == "__main__":
    asyncio.run(main())