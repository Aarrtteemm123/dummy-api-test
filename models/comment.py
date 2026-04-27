from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class CommentUser:
    id: int
    username: str
    fullname: str


@dataclass(slots=True)
class Comment:
    id: int
    body: str
    post_id: int
    likes: int
    user: CommentUser

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "Comment":
        u = data["user"]
        return cls(
            id=int(data["id"]),
            body=str(data["body"]),
            post_id=int(data["postId"]),
            # API may omit likes on some payloads; default keeps the model usable.
            likes=int(data.get("likes", 0)),
            user=CommentUser(
                id=int(u["id"]),
                username=str(u["username"]),
                fullname=str(u.get("fullName", "")),
            ),
        )
