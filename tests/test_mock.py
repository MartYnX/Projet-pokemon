"""
_summary
"""
from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)

def test_return_double(mocker):
    """
    _summary
    """
    mocker.patch(
        "main.get_double",
        return_value=10
    )
    response = client.get("/5")
    assert response.status_code == 200
