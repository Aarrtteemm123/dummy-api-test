import asyncio
from dummy_client import DummyClient
from storage import InMemoryStorage
from post_service import PostService


async def main():
    async with DummyClient() as client:
        storage = InMemoryStorage()
        service = PostService(client, storage)

        await service.fetch_and_store_post(1)
        await service.search_and_store_posts("love")
        await service.fetch_and_store_comments(1)

        print("Stored posts:", storage.list_collection("posts"))
        print("Stored comments:", storage.list_collection("comments"))


if __name__ == "__main__":
    asyncio.run(main())