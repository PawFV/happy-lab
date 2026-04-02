"""Functional tests for VulnBank — verifies routes, auth, and CRUD work correctly."""

from io import BytesIO
from conftest import login


class TestRoutes:
    def test_index_returns_200(self, client):
        r = client.get("/")
        assert r.status_code == 200
        assert b"SecBank" in r.data

    def test_login_page_renders(self, client):
        r = client.get("/login")
        assert r.status_code == 200
        assert b"Login" in r.data

    def test_register_page_renders(self, client):
        r = client.get("/register")
        assert r.status_code == 200

    def test_posts_page_renders(self, client):
        r = client.get("/posts")
        assert r.status_code == 200

    def test_search_page_renders(self, client):
        r = client.get("/search")
        assert r.status_code == 200

    def test_upload_page_renders(self, client):
        r = client.get("/upload")
        assert r.status_code == 200

    def test_download_page_renders(self, client):
        r = client.get("/download")
        assert r.status_code == 200

    def test_robots_txt(self, client):
        r = client.get("/robots.txt")
        assert r.status_code == 200
        assert b"User-agent" in r.data

    def test_debug_page_renders(self, client):
        r = client.get("/debug")
        assert r.status_code == 200

    def test_admin_users_page_renders(self, client):
        r = client.get("/admin/users")
        assert r.status_code == 200

    def test_backup_returns_file(self, client):
        r = client.get("/backup")
        assert r.status_code == 200


class TestAuth:
    def test_valid_login_redirects_to_profile(self, client):
        r = login(client)
        assert r.status_code == 302
        assert "/profile" in r.headers.get("Location", "")

    def test_invalid_login_stays_on_page(self, client):
        r = client.post("/login", data={"username": "admin", "password": "wrong"})
        assert r.status_code == 200
        assert b"Invalid credentials" in r.data

    def test_logout_redirects(self, client):
        login(client)
        r = client.get("/logout")
        assert r.status_code == 302

    def test_profile_redirects_when_not_logged_in(self, client):
        r = client.get("/profile")
        assert r.status_code == 302

    def test_profile_renders_when_logged_in(self, client):
        login(client)
        r = client.get("/profile", follow_redirects=True)
        assert r.status_code == 200
        assert b"admin" in r.data

    def test_register_new_user(self, client):
        r = client.post("/register", data={
            "username": "newuser",
            "password": "pass123",
            "email": "new@test.local",
        })
        assert r.status_code == 200
        assert b"User created" in r.data

    def test_register_duplicate_shows_error(self, client):
        r = client.post("/register", data={
            "username": "admin",
            "password": "pass",
            "email": "dup@test.local",
        })
        assert r.status_code == 200
        assert b"Error" in r.data


class TestSearch:
    def test_search_with_query_returns_200(self, client):
        r = client.get("/search?q=Welcome")
        assert r.status_code == 200

    def test_search_no_results(self, client):
        r = client.get("/search?q=nonexistent_xyzzy")
        assert r.status_code == 200
        assert b"No results found" in r.data

    def test_search_finds_post(self, client):
        r = client.get("/search?q=Welcome")
        assert r.status_code == 200
        assert b"Welcome" in r.data


class TestPosts:
    def test_posts_shows_seeded_data(self, client):
        r = client.get("/posts")
        assert r.status_code == 200
        assert b"Welcome" in r.data

    def test_create_post_requires_login(self, client):
        r = client.post("/posts", data={"title": "Test", "content": "Body"})
        assert r.status_code == 200

    def test_create_post_when_logged_in(self, client):
        login(client)
        client.post("/posts", data={"title": "My Post", "content": "Hello world"})
        r = client.get("/posts")
        assert b"My Post" in r.data


class TestUpload:
    def test_upload_requires_login(self, client):
        data = {"file": (BytesIO(b"content"), "test.txt")}
        r = client.post("/upload", data=data, content_type="multipart/form-data")
        assert r.status_code == 302

    def test_upload_file_when_logged_in(self, client):
        login(client)
        data = {"file": (BytesIO(b"hello"), "test.txt")}
        r = client.post("/upload", data=data, content_type="multipart/form-data")
        assert r.status_code == 200
        assert b"Document uploaded" in r.data


class TestProfile:
    def test_profile_by_id(self, client):
        r = client.get("/profile/1")
        assert r.status_code == 200
        assert b"admin" in r.data

    def test_profile_nonexistent_returns_404(self, client):
        r = client.get("/profile/999")
        assert r.status_code == 404
