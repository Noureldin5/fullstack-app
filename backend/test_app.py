import pytest
from unittest.mock import patch, MagicMock
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def make_mock_db(fetchall=None, fetchone=None):
    """Helper: return a mock connection/cursor pair."""
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_conn.cursor.return_value = mock_cur
    if fetchall is not None:
        mock_cur.fetchall.return_value = fetchall
    if fetchone is not None:
        mock_cur.fetchone.return_value = fetchone
    return mock_conn


def test_get_data_returns_list(client):
    with patch("app.get_db", return_value=make_mock_db(fetchall=[(1, "Buy milk"), (2, "Fix tests")])):
        res = client.get("/api/data")
    assert res.status_code == 200
    data = res.get_json()
    assert len(data) == 2
    assert data[0]["title"] == "Buy milk"


def test_add_data_success(client):
    with patch("app.get_db", return_value=make_mock_db(fetchone=(42,))):
        res = client.post("/api/data", json={"title": "New task"})
    assert res.status_code == 201
    assert res.get_json()["id"] == 42


def test_add_data_empty_title_rejected(client):
    res = client.post("/api/data", json={"title": "  "})
    assert res.status_code == 400


def test_add_data_missing_body_rejected(client):
    res = client.post("/api/data", json={})
    assert res.status_code == 400


def test_delete_data_success(client):
    with patch("app.get_db", return_value=make_mock_db(fetchone=(1,))):
        res = client.delete("/api/data/1")
    assert res.status_code == 200
    assert res.get_json()["deleted"] == 1


def test_delete_data_not_found(client):
    with patch("app.get_db", return_value=make_mock_db(fetchone=None)):
        res = client.delete("/api/data/999")
    assert res.status_code == 404
