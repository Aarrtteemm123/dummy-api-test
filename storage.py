from collections.abc import Iterable
from typing import Any, Dict


class InMemoryStorage:
    def __init__(self) -> None:
        self._db: Dict[str, Dict[Any, Any]] = {}

    def create(self, collection: str, key: Any, record: Any) -> None:
        self._db.setdefault(collection, {})
        self._db[collection][key] = record

    def create_many(self, collection: str, pairs: Iterable[tuple[Any, Any]]) -> None:
        bucket = self._db.setdefault(collection, {})
        for key, record in pairs:
            bucket[key] = record

    def read(self, collection: str, key: Any) -> Any:
        return self._db.get(collection, {}).get(key)

    def update(self, collection: str, key: Any, record: Any) -> None:
        if collection in self._db and key in self._db[collection]:
            self._db[collection][key] = record

    def delete(self, collection: str, key: Any) -> None:
        if collection in self._db and key in self._db[collection]:
            self._db[collection].pop(key, None)

    def list_collection(self, collection: str) -> Dict[Any, Any]:
        return dict(self._db.get(collection, {}))
