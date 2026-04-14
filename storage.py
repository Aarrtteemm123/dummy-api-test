from collections.abc import Iterable
from typing import Any, Dict, Protocol


class Storage(Protocol):
    def create(self, collection: str, key: Any, value: Any) -> None: ...

    def create_many(
        self, collection: str, pairs: Iterable[tuple[Any, Any]]
    ) -> None: ...

    def read(self, collection: str, key: Any) -> Any: ...

    def update(self, collection: str, key: Any, value: Any) -> None: ...

    def delete(self, collection: str, key: Any) -> None: ...

    def list_collection(self, collection: str) -> Dict[Any, Any]: ...


class InMemoryStorage:
    def __init__(self):
        self._db: Dict[str, Dict[Any, Any]] = {}

    def create(self, collection: str, key: Any, value: Any) -> None:
        self._db.setdefault(collection, {})
        self._db[collection][key] = value

    def create_many(
        self, collection: str, pairs: Iterable[tuple[Any, Any]]
    ) -> None:
        bucket = self._db.setdefault(collection, {})
        for key, value in pairs:
            bucket[key] = value

    def read(self, collection: str, key: Any) -> Any:
        return self._db.get(collection, {}).get(key)

    def update(self, collection: str, key: Any, value: Any) -> None:
        if collection in self._db and key in self._db[collection]:
            self._db[collection][key] = value

    def delete(self, collection: str, key: Any) -> None:
        if collection in self._db and key in self._db[collection]:
            del self._db[collection][key]

    def list_collection(self, collection: str) -> Dict[Any, Any]:
        return dict(self._db.get(collection, {}))
