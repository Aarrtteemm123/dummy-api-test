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
    def from_data(cls, payload: dict[str, Any]) -> "Comment":
        user_payload = payload["user"]
        return cls(
            id=int(payload["id"]),
            body=str(payload["body"]),
            post_id=int(payload["postId"]),
            likes=int(payload.get("likes", 0)),
            user=CommentUser(
                id=int(user_payload["id"]),
                username=str(user_payload["username"]),
                fullname=str(user_payload.get("fullName", "")),
            ),
        )
