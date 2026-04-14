import pytest

from storage import InMemoryStorage


def test_create_read_roundtrip() -> None:
    s = InMemoryStorage()
    s.create("items", 1, "a")
    assert s.read("items", 1) == "a"
    assert s.read("items", 99) is None


def test_create_many_single_bucket() -> None:
    s = InMemoryStorage()
    s.create_many("x", [(1, "one"), (2, "two")])
    assert s.list_collection("x") == {1: "one", 2: "two"}


def test_update_only_existing_key() -> None:
    s = InMemoryStorage()
    s.update("items", 1, "x")
    assert s.read("items", 1) is None
    s.create("items", 1, "a")
    s.update("items", 1, "b")
    assert s.read("items", 1) == "b"


def test_delete_existing() -> None:
    s = InMemoryStorage()
    s.create("items", 1, "a")
    s.delete("items", 1)
    assert s.read("items", 1) is None


def test_list_collection_returns_copy() -> None:
    s = InMemoryStorage()
    s.create("items", 1, "a")
    outer = s.list_collection("items")
    outer[1] = "mutated"
    assert s.read("items", 1) == "a"


@pytest.mark.parametrize(
    "method,args",
    [
        ("read", ("missing", 1)),
        ("list_collection", ("missing",)),
    ],
)
def test_missing_collection_safe(method: str, args: tuple) -> None:
    s = InMemoryStorage()
    fn = getattr(s, method)
    assert fn(*args) in (None, {})
