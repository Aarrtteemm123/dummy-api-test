from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class Post:
    # Field names mirror DummyJSON (camelCase userId); extra keys in JSON are ignored.
    id: int
    title: str
    body: str
    tags: list[str]
    userId: int

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "Post":
        tags_raw = data.get("tags") or []
        # Coerce elements to str so malformed or mixed-type payloads still produce a list[str].
        tags = [str(t) for t in tags_raw]
        return cls(
            id=int(data["id"]),
            title=str(data["title"]),
            body=str(data["body"]),
            tags=tags,
            userId=int(data["userId"]),
        )
