"""Main application entry point."""

from flask import Flask
from routes import register_routes
from middleware import setup_middleware
from config import Config


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    setup_middleware(app)
    register_routes(app)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=Config.DEBUG, port=Config.PORT)
