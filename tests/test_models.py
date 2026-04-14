import pytest

from models.comment import Comment, CommentUser
from models.post import Post


def test_post_from_data_minimal() -> None:
    p = Post.from_data(
        {
            "id": 1,
            "title": "t",
            "body": "b",
            "tags": ["x", "y"],
            "userId": 42,
            "reactions": {"ignored": True},
        }
    )
    assert p == Post(
        id=1,
        title="t",
        body="b",
        tags=["x", "y"],
        userId=42,
    )


def test_post_from_data_tags_missing_or_coerced() -> None:
    p = Post.from_data(
        {
            "id": 1,
            "title": "",
            "body": "",
            "userId": 0,
        }
    )
    assert p.tags == []
    p2 = Post.from_data(
        {
            "id": 1,
            "title": "",
            "body": "",
            "tags": [1, 2],
            "userId": 0,
        }
    )
    assert p2.tags == ["1", "2"]


def test_comment_from_data() -> None:
    c = Comment.from_data(
        {
            "id": 10,
            "body": "hello",
            "postId": 3,
            "likes": 5,
            "user": {
                "id": 7,
                "username": "u",
                "fullName": "Full",
            },
        }
    )
    assert c == Comment(
        id=10,
        body="hello",
        postId=3,
        likes=5,
        user=CommentUser(id=7, username="u", fullName="Full"),
    )


def test_comment_likes_and_fullname_defaults() -> None:
    c = Comment.from_data(
        {
            "id": 1,
            "body": "b",
            "postId": 1,
            "user": {"id": 1, "username": "x"},
        }
    )
    assert c.likes == 0
    assert c.user.fullName == ""


def test_post_from_data_missing_required_raises() -> None:
    with pytest.raises(KeyError):
        Post.from_data({"id": 1})
