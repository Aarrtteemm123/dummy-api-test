import asyncio
import logging

import httpx

from clients.dummy_client import DummyClient
from services.post_service import PostService
from storage import InMemoryStorage

logger = logging.getLogger(__name__)


async def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    try:
        # Context manager ensures the underlying httpx client is closed even on errors.
        async with DummyClient() as client:
            storage = InMemoryStorage()
            service = PostService(client, storage)

            post = await service.fetch_post(1)
            service.save_post(post, storage_key=1)

            posts = await service.fetch_posts_by_query("love")
            service.save_posts(posts)

            comments = await service.fetch_comments(2)
            service.save_comments(comments)

            logger.info("Stored posts: %s", storage.list_collection("posts"))
            logger.info("Stored comments: %s", storage.list_collection("comments"))
    except httpx.HTTPStatusError as http_error:
        status = http_error.response.status_code
        url = http_error.request.url
        logger.error("HTTP %s for %r", status, url)
    except httpx.RequestError as request_error:
        logger.error("RequestError: %s", request_error)
    except Exception as error:
        logger.error("Error: %s", error)


if __name__ == "__main__":
    asyncio.run(main())
