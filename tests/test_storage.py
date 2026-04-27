import pytest

from storage import InMemoryStorage


def test_create_read_roundtrip() -> None:
    mem_storage = InMemoryStorage()
    mem_storage.create("items", 1, "a")
    assert mem_storage.read("items", 1) == "a"
    assert mem_storage.read("items", 99) is None


def test_create_many_single_bucket() -> None:
    mem_storage = InMemoryStorage()
    mem_storage.create_many("x", [(1, "one"), (2, "two")])
    assert mem_storage.list_collection("x") == {1: "one", 2: "two"}


def test_update_only_existing_key() -> None:
    mem_storage = InMemoryStorage()
    mem_storage.update("items", 1, "x")
    assert mem_storage.read("items", 1) is None
    mem_storage.create("items", 1, "a")
    mem_storage.update("items", 1, "b")
    assert mem_storage.read("items", 1) == "b"


def test_delete_existing() -> None:
    mem_storage = InMemoryStorage()
    mem_storage.create("items", 1, "a")
    mem_storage.delete("items", 1)
    assert mem_storage.read("items", 1) is None


def test_list_collection_returns_copy() -> None:
    mem_storage = InMemoryStorage()
    mem_storage.create("items", 1, "a")
    outer = mem_storage.list_collection("items")
    outer[1] = "mutated"
    assert mem_storage.read("items", 1) == "a"


@pytest.mark.parametrize(
    "method,args",
    [
        ("read", ("missing", 1)),
        ("list_collection", ("missing",)),
    ],
)
def test_missing_collection_safe(method: str, args: tuple) -> None:
    mem_storage = InMemoryStorage()
    fn = getattr(mem_storage, method)
    assert fn(*args) in (None, {})
