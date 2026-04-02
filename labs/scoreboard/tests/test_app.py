def test_index_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Lab CTF Scoreboard" in response.data

def test_submit_valid_flag(client):
    response = client.post(
        "/submit",
        data={"team": "test_team", "flag": "FLAG{test_flag}"},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Flag accepted! 100 points awarded to test_team." in response.data
    assert b"test_team" in response.data

def test_submit_invalid_flag(client):
    response = client.post(
        "/submit",
        data={"team": "test_team", "flag": "NOT_A_FLAG"},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Invalid flag format." in response.data

def test_submit_duplicate_flag(client):
    # First submit
    client.post(
        "/submit",
        data={"team": "test_team", "flag": "FLAG{test_flag}"}
    )
    # Duplicate submit
    response = client.post(
        "/submit",
        data={"team": "test_team", "flag": "FLAG{test_flag}"},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Flag already submitted by your team!" in response.data

def test_admin_page(client):
    response = client.get("/admin")
    assert response.status_code == 200
    assert b"Generate Dynamic Vulnerabilities" in response.data

def test_generate_requires_api_key(client):
    response = client.post("/admin/generate", data={"provider": "openai", "api_key": ""}, follow_redirects=True)
    assert response.status_code == 200
    assert b"API Key is required." in response.data