import requests
import pytest
import base64
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src", "Database_management_microservice"))
from database_management_microservice import app, db



CATALOGUE_URL = "http://localhost:3000"
DATABASE_URL = "http://localhost:3002"

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
def test_add_valid_track(sample_track):
    """Test that a valid track can be added successfully."""
    response = requests.post(f"{CATALOGUE_URL}/tracks", json=sample_track)
    assert response.status_code == 201

    # Verify the track is in the database
    tracks_response = requests.get(f"{DATABASE_URL}/db/tracks")
    assert tracks_response.status_code == 200
    tracks = tracks_response.json()
    assert any(track["title"] == sample_track["title"] for track in tracks)


#Unhappy Paths
def test_add_track_missing_fields():
    """Test that adding a track with missing fields returns a 400 error."""
    incomplete_track = {"title": "Incomplete Song"}
    response = requests.post(f"{CATALOGUE_URL}/tracks", json=incomplete_track)
    assert response.status_code == 400

def test_duplicate_track(sample_track):
    """Test that adding the same track twice is handled correctly."""
    requests.post(f"{CATALOGUE_URL}/tracks", json=sample_track)

    response = requests.post(f"{CATALOGUE_URL}/tracks", json=sample_track)
    assert response.status_code == 409

def test_add_track_database_unreachable(monkeypatch, sample_track):
    client = app.test_client()

    def fake_insert(data):
        raise Exception("Simulated database failure")
    monkeypatch.setattr(db, "insert", fake_insert)

    response = client.post("/db/tracks", json=sample_track)
    assert response.status_code == 503
