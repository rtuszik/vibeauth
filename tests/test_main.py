from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from lma.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "<h1>LMA</h1>" in response.text

@patch('litellm.acompletion')
def test_get_signin_modal(mock_acompletion):
    mock_acompletion.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content='<form action="/check-vibe" method="post"><textarea name="user_input"></textarea><button type="submit">Submit</button></form>'))]
    )
    response = client.post("/get-signin-modal")
    assert response.status_code == 200
    assert "<form" in response.text

@patch('litellm.acompletion')
def test_check_vibe_granted(mock_acompletion):
    mock_acompletion.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content='ACCESS GRANTED'))]
    )
    response = client.post("/check-vibe", data={"user_input": "test"})
    assert response.status_code == 200
    assert "<h1>Vibe Check: PASSED</h1>" in response.text

@patch('litellm.acompletion')
def test_check_vibe_denied(mock_acompletion):
    mock_acompletion.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content='ACCESS DENIED'))]
    )
    response = client.post("/check-vibe", data={"user_input": "test"})
    assert response.status_code == 200
    assert "<h1>Vibe Check: FAILED</h1>" in response.text
