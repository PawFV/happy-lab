import os
import sys
import tempfile

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


@pytest.fixture()
def client(monkeypatch, tmp_path):
    db_file = tmp_path / "test_vulnbank.db"
    backup_file = tmp_path / "backup.sql"

    # Use SQLite for testing since Docker/MySQL may not be running locally
    monkeypatch.setenv("USE_SQLITE", "1")
    monkeypatch.setenv("SQLITE_PATH", str(db_file))
    monkeypatch.setenv("DATABASE_BACKUP_FILE", str(backup_file))
    
    # Ensure MySQL env vars are explicitly cleared/ignored for the test
    monkeypatch.delenv("MYSQL_HOST", raising=False)

    import importlib
    import db as db_module
    importlib.reload(db_module)

    from app import create_app

    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as c:
        yield c


def login(client, username="admin", password="admin123"):
    return client.post(
        "/login",
        data={
            "username": username,
            "password": password,
        },
    )
