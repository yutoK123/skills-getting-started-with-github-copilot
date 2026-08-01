import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture(autouse=True)
def reset_activities():
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(original)


@pytest.fixture
def client():
    return TestClient(app)


def test_unregister_participant_from_activity(client):
    response = client.delete(
        "/activities/Chess Club/participants?email=michael@mergington.edu"
    )

    assert response.status_code == 200
    assert "Removed michael@mergington.edu" in response.json()["message"]

    updated_activities = client.get("/activities").json()
    assert "michael@mergington.edu" not in updated_activities["Chess Club"]["participants"]


def test_unregister_participant_returns_error_for_unknown_student(client):
    response = client.delete(
        "/activities/Chess Club/participants?email=ghost@mergington.edu"
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not signed up for this activity"
