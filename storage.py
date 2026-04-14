from collections.abc import Iterable
from typing import Any, Dict


class InMemoryStorage:
    def __init__(self):
        self._db: Dict[str, Dict[Any, Any]] = {}

    def create(self, collection: str, key: Any, value: Any) -> None:
        self._db.setdefault(collection, {})
        self._db[collection][key] = value

    def create_many(
        self, collection: str, pairs: Iterable[tuple[Any, Any]]
    ) -> None:
        # One setdefault per batch; avoids repeating it for every row in the same collection.
        bucket = self._db.setdefault(collection, {})
        for key, value in pairs:
            bucket[key] = value

    def read(self, collection: str, key: Any) -> Any:
        return self._db.get(collection, {}).get(key)

    def update(self, collection: str, key: Any, value: Any) -> None:
        # No insert: missing collection/key is a silent no-op (upsert is not create).
        if collection in self._db and key in self._db[collection]:
            self._db[collection][key] = value

    def delete(self, collection: str, key: Any) -> None:
        if collection in self._db and key in self._db[collection]:
            del self._db[collection][key]

    def list_collection(self, collection: str) -> Dict[Any, Any]:
        # Shallow copy so callers cannot mutate our internal bucket dict.
        return dict(self._db.get(collection, {}))
