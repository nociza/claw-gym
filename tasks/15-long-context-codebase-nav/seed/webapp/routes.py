"""API route handlers."""

from flask import Flask, jsonify, request, g
from exceptions import NotFoundError, ValidationError
from services import UserService, PostService


def register_routes(app: Flask) -> None:
    """Register all API routes."""

    @app.route("/health")
    def health():
        return jsonify({"status": "ok"})

    # --- User routes ---
    @app.route("/api/users", methods=["GET"])
    def list_users():
        users = UserService.list_all()
        return jsonify([u.__dict__ for u in users])

    @app.route("/api/users/<int:user_id>", methods=["GET"])
    def get_user(user_id):
        user = UserService.get_by_id(user_id)
        if not user:
            raise NotFoundError("User", str(user_id))
        return jsonify(user.__dict__)

    @app.route("/api/auth/login", methods=["POST"])
    def login():
        data = request.get_json()
        if not data or "email" not in data or "password" not in data:
            raise ValidationError("Email and password required")
        token = UserService.authenticate(data["email"], data["password"])
        return jsonify({"token": token})

    @app.route("/api/auth/register", methods=["POST"])
    def register():
        data = request.get_json()
        required = ["email", "name", "password"]
        missing = [f for f in required if f not in (data or {})]
        if missing:
            raise ValidationError(f"Missing fields: {', '.join(missing)}")
        user = UserService.create(data["email"], data["name"], data["password"])
        return jsonify({"id": user.id, "email": user.email}), 201

    # --- Post routes ---
    @app.route("/api/posts", methods=["GET"])
    def list_posts():
        posts = PostService.list_published()
        return jsonify([p.__dict__ for p in posts])

    @app.route("/api/posts/<int:post_id>", methods=["GET"])
    def get_post(post_id):
        post = PostService.get_by_id(post_id)
        if not post:
            raise NotFoundError("Post", str(post_id))
        return jsonify(post.__dict__)

    @app.route("/api/posts", methods=["POST"])
    def create_post():
        data = request.get_json()
        if not data or "title" not in data or "content" not in data:
            raise ValidationError("Title and content required")
        post = PostService.create(
            title=data["title"],
            content=data["content"],
            author_id=g.current_user["user_id"],
        )
        return jsonify({"id": post.id}), 201
