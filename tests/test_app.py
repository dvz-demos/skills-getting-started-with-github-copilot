import pytest


def test_get_activities_returns_activity_list(client):
    # Arrange

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    body = response.json()
    assert "Chess Club" in body
    assert "Programming Class" in body
    assert body["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"
    assert isinstance(body["Chess Club"]["participants"], list)


def test_signup_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "tester@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    response = client.get("/activities")
    assert email in response.json()[activity_name]["participants"]


def test_duplicate_signup_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_unregister_removes_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "daniel@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/unregister?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity_name}"

    response = client.get("/activities")
    assert email not in response.json()[activity_name]["participants"]


def test_unregister_missing_participant_returns_404(client):
    # Arrange
    activity_name = "Chess Club"
    email = "ghost@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/unregister?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
