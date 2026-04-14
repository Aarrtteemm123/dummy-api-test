from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class Post:
    id: int
    title: str
    body: str
    tags: list[str]
    userId: int

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "Post":
        tags_raw = data.get("tags") or []
        tags = [str(t) for t in tags_raw]
        return cls(
            id=int(data["id"]),
            title=str(data["title"]),
            body=str(data["body"]),
            tags=tags,
            userId=int(data["userId"]),
        )
