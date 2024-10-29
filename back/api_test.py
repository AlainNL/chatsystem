from urllib import response
import requests
import pytest

BASE_URL = "http://127.0.0.1:5000/chat"

# Testing valid chat history
def test_valid_chat_history():
    history = [
        {"sender": "user", "message": "Hello!"},
        {"sender": "agent", "message": "How can I help you?"}
    ]
    response = requests.post(BASE_URL, json={"history": history})
    assert response.status_code == 200
    assert "agent_reply" in response.json()

# Testing empty chat history
def test_empty_chat_history():
    response = requests.post(BASE_URL, json={"history": []})
    assert response.status_code == 200
    assert  "agent_reply" in response.json()

# Testing invalid history type
def test_invalid_history_type():
    response = requests.post(BASE_URL, json={"history": "invalid data"})
    assert response.status_code == 400
    assert response.json() == {"error": "Incorrect chat history"}

# Testing with a invalid sender history
def test_invalid_sender():
    history = [
        {"sender": "user", "message": "Hello"},
        {"sender": "invalid_sender", "message" : "This is shouln't work"}
    ]
    response = requests.post(BASE_URL, json={"history" : history})
    response.status_code == 400
    response.json() == {"error": "Incorrect chat history"}

# Testing with a history that doesn't alternate correctly
def test_sender_not_alternating():
    history = [
        {"sender": "user", "message": "Hello!"},
        {"sender": "user", "message": "Are you here ?"},
    ]
    response = requests.post(BASE_URL, json={"history": history})
    assert response.status_code == 400
    assert response.json() == {"error": "Incorrect chat history"}

# Testing with a wrond message structure
def test_no_history_message_structure():
    history = [
        "Hello, this is a string"
    ]
    response = requests.post(BASE_URL, json={"history": history})
    assert response.status_code == 400
    assert response.json() == {"error": "Incorrect chat history"}
