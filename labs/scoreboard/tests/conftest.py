import os
import sys
import tempfile

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

@pytest.fixture
def app():
    # Set a temporary file for scores data
    fd, path = tempfile.mkstemp()
    os.environ["DATA_FILE"] = path
    
    # Needs to be imported after env var is set if we want it to pick it up, 
    # but app.py initializes it globally so we might need to patch it directly.
    import app as flask_app
    flask_app.DATA_FILE = path
    
    flask_app.app.config["TESTING"] = True
    yield flask_app.app
    
    os.close(fd)
    os.unlink(path)

@pytest.fixture
def client(app):
    return app.test_client()