import requests
import pytest
import base64
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src", "Database_management_microservice"))
from database_management_microservice import app, db
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src", "Catalogue_management_microservice"))
from catalogue_management_microservice import app as catalogue_app

CATALOGUE_URL = "http://localhost:3000"
DATABASE_URL = "http://localhost:3001"

@pytest.fixture
def sample_track():
    return {
        "title": "Dont Look Back in Anger",
        "encoded_track": encode_audio_to_base64("./Music/Tracks/Dont Look Back in Anger.wav")
    }

@pytest.fixture(autouse=True)
def reset_database():
    """Ensures the database is cleared after every test."""
    yield
    requests.post(f"{DATABASE_URL}/db/reset")

#Helper Function
def encode_audio_to_base64(file_path):
    """Reads a WAV file and encodes it to a base64 string."""
    with open(file_path, "rb") as audio_file:
        encoded_string = base64.b64encode(audio_file.read()).decode("utf-8")
    return encoded_string

#Happy Paths
def test_delete_existing_track(sample_track):
    """Test that an existing track can be deleted successfully."""
    add_response = requests.post(f"{DATABASE_URL}/db/tracks", json=sample_track)
    assert add_response.status_code == 201

    delete_response = requests.delete(f"{CATALOGUE_URL}/tracks/{sample_track['title']}")
    assert delete_response.status_code == 200

    tracks_response = requests.get(f"{DATABASE_URL}/db/tracks")
    assert tracks_response.status_code == 200
    tracks = tracks_response.json()
    assert not any(track["title"] == sample_track["title"] for track in tracks)

#Unhappy Paths
def test_delete_nonexistent_track():
    """Test that deleting a non-existent track returns a 404 error."""
    response = requests.delete(f"{CATALOGUE_URL}/tracks/NonExistentTrack")
    assert response.status_code == 404

def test_delete_no_title():
    """Test that attempting to delete without a title returns a 400 error."""
    response = requests.delete(f"{CATALOGUE_URL}/tracks/")
    assert response.status_code == 400

def test_delete_track_database_unreachable(monkeypatch, sample_track):
    """
    Test that deleting a track via the catalogue microservice returns a 503 when the database is unreachable.
    """
    # Import the catalogue microservice's app
    from catalogue_management_microservice import app as catalogue_app
    client = catalogue_app.test_client()

    # Add the track normally using the catalogue endpoint.
    add_response = client.post("/tracks", json=sample_track)
    assert add_response.status_code == 201

    # Monkeypatch requests.delete so that when the catalogue service calls it, it simulates a database failure.
    def fake_requests_delete(url, *args, **kwargs):
        class FakeResponse:
            status_code = 503
            def json(self):
                return {}
        return FakeResponse()
    monkeypatch.setattr(requests, "delete", fake_requests_delete)

    # Attempt to delete the track via the catalogue microservice.
    response = client.delete(f"/tracks/{sample_track['title']}")
    assert response.status_code == 503
