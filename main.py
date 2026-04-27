import asyncio
import sys

import httpx

from clients.dummy_client import DummyClient
from services.post_service import PostService
from storage import InMemoryStorage


async def main() -> None:
    try:
        # Context manager ensures the underlying httpx client is closed even on errors.
        async with DummyClient() as client:
            storage = InMemoryStorage()
            service = PostService(client, storage)

            await service.download_into_storage_by_post_id(1)
            await service.download_into_storage_by_query("love")
            await service.download_comment_into_storage_by_post_id(2)
            print("Stored posts:", storage.list_collection("posts"))
            print("Stored comments:", storage.list_collection("comments"))
    # 4xx/5xx after raise_for_status() on the client.
    except httpx.HTTPStatusError as exc:
        print(
            f"HTTP {exc.response.status_code} for {exc.request.url!r}",
            file=sys.stderr,
        )
    # Transport-level failures (DNS, timeout, connection reset, etc.).
    except httpx.RequestError as exc:
        print(f"RequestError: {exc}", file=sys.stderr)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)


if __name__ == "__main__":
    asyncio.run(main())