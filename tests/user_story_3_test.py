import requests
import pytest
import base64
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src", "Database_management_microservice"))
from database_management_microservice import app, db

CATALOGUE_URL = "http://localhost:3000"
DATABASE_URL = "http://localhost:3001"

@pytest.fixture
def sample_tracks():
    return [
        {"title": "Everybody (Backstreets Back) (Radio Edit)", "encoded_track": encode_audio_to_base64("./Music/Tracks/Everybody (Backstreets Back) (Radio Edit).wav")},
        {"title": "good 4 u", "encoded_track": encode_audio_to_base64("./Music/Tracks/good 4 u.wav")}
    ]

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

# Happy Paths
def test_list_tracks_non_empty(sample_tracks):
    """Test that listing tracks returns all added tracks."""
    # Add sample tracks
    for track in sample_tracks:
        requests.post(f"{CATALOGUE_URL}/tracks", json=track)

    # Fetch all tracks
    response = requests.get(f"{CATALOGUE_URL}/tracks")
    assert response.status_code == 200

    # Verify all added tracks are in the response
    tracks = response.json()
    track_titles = {track["title"] for track in tracks}
    expected_titles = {track["title"] for track in sample_tracks}
    assert expected_titles.issubset(track_titles)

#Unhappy Paths
def test_list_tracks_empty():
    """Test that listing tracks when there are none returns an empty list."""
    response = requests.get(f"{CATALOGUE_URL}/tracks")
    assert response.status_code == 200
    assert response.json() == []

def test_list_tracks_database_unreachable(monkeypatch):
    """
    Test that listing tracks returns a 503 when the database is unreachable.
    """
    client = app.test_client()

    # Monkeypatch db.get_all_tracks to simulate a database failure
    def fake_get_all_tracks():
        raise Exception("Simulated database failure")
    monkeypatch.setattr(db, "get_all_tracks", fake_get_all_tracks)

    # Attempt to fetch all tracks
    response = client.get("/db/tracks")
    assert response.status_code == 503
    data = response.get_json()
    assert data.get("error") == "Database unreachable"
