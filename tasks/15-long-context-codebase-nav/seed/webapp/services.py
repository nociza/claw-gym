"""Business logic services."""

import hashlib
from typing import Optional
from models import User, Post
from auth import create_token
from exceptions import AuthenticationError, NotFoundError, ConflictError

# In-memory storage (would be a database in production)
_users: dict[int, User] = {}
_posts: dict[int, Post] = {}
_next_user_id = 1
_next_post_id = 1


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


class UserService:
    @staticmethod
    def create(email: str, name: str, password: str) -> User:
        global _next_user_id
        for u in _users.values():
            if u.email == email:
                raise ConflictError(f"User with email '{email}' already exists")
        user = User(
            id=_next_user_id,
            email=email,
            name=name,
            password_hash=_hash_password(password),
        )
        _users[user.id] = user
        _next_user_id += 1
        return user

    @staticmethod
    def get_by_id(user_id: int) -> Optional[User]:
        return _users.get(user_id)

    @staticmethod
    def list_all() -> list[User]:
        return list(_users.values())

    @staticmethod
    def authenticate(email: str, password: str) -> str:
        for user in _users.values():
            if user.email == email:
                if user.password_hash == _hash_password(password):
                    return create_token(user.id, user.email)
                raise AuthenticationError("Invalid password")
        raise AuthenticationError("User not found")


class PostService:
    @staticmethod
    def create(title: str, content: str, author_id: int) -> Post:
        global _next_post_id
        if not _users.get(author_id):
            raise NotFoundError("Author", str(author_id))
        post = Post(
            id=_next_post_id,
            title=title,
            content=content,
            author_id=author_id,
        )
        _posts[post.id] = post
        _next_post_id += 1
        return post

    @staticmethod
    def get_by_id(post_id: int) -> Optional[Post]:
        return _posts.get(post_id)

    @staticmethod
    def list_published() -> list[Post]:
        return [p for p in _posts.values() if p.published]
