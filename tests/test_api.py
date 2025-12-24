from fastapi.testclient import TestClient
from app.api.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert '<h1 class="site-title">' in response.text

def test_read_admin_page():
    response = client.get("/admin")
    assert response.status_code == 200
    assert 'Admin Panel' in response.text

def test_static_css_file_is_reachable():
    response = client.get("/static/css/style.css")
    assert response.status_code == 200
    assert "text/css" in response.headers["content-type"]
