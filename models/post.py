from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class Post:
    id: int
    title: str
    body: str
    tags: list[str]
    user_id: int

    @classmethod
    def from_data(cls, payload: dict[str, Any]) -> "Post":
        tags_raw = payload.get("tags") or []
        tags = [str(tag) for tag in tags_raw]
        return cls(
            id=int(payload["id"]),
            title=str(payload["title"]),
            body=str(payload["body"]),
            tags=tags,
            user_id=int(payload["userId"]),
        )
