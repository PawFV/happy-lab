# Vulnerable Flask App — SecLab
# INTENTIONALLY INSECURE — For isolated network use only

from flask import Flask, g

from db import init_db
from routes import register_routes


def create_app():
    app = Flask(__name__)
    # VULNERABILITY: weak and hardcoded key
    app.secret_key = "super_secret_key_123"

    @app.teardown_appcontext
    def close_db(exception):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    register_routes(app)

    with app.app_context():
        init_db()

    return app


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=5000, debug=True)  # VULNERABLE: debug=True
