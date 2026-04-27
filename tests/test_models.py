import pytest

from models.comment import Comment, CommentUser
from models.post import Post


def test_post_from_data_minimal() -> None:
    post = Post.from_data(
        {
            "id": 1,
            "title": "t",
            "body": "b",
            "tags": ["x", "y"],
            "userId": 42,
            "reactions": {"ignored": True},
        }
    )
    assert post == Post(
        id=1,
        title="t",
        body="b",
        tags=["x", "y"],
        user_id=42,
    )


def test_post_from_data_tags_missing_or_coerced() -> None:
    post = Post.from_data(
        {
            "id": 1,
            "title": "",
            "body": "",
            "userId": 0,
        }
    )
    assert post.tags == []
    post2 = Post.from_data(
        {
            "id": 1,
            "title": "",
            "body": "",
            "tags": [1, 2],
            "userId": 0,
        }
    )
    assert post2.tags == ["1", "2"]


def test_comment_from_data() -> None:
    comment = Comment.from_data(
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
    assert comment == Comment(
        id=10,
        body="hello",
        post_id=3,
        likes=5,
        user=CommentUser(id=7, username="u", fullname="Full"),
    )


def test_comment_likes_and_fullname_defaults() -> None:
    comment = Comment.from_data(
        {
            "id": 1,
            "body": "b",
            "postId": 1,
            "user": {"id": 1, "username": "x"},
        }
    )
    assert comment.likes == 0
    assert comment.user.fullname == ""


def test_post_from_data_missing_required_raises() -> None:
    with pytest.raises(KeyError):
        Post.from_data({"id": 1})
