import requests
import pytest
import base64

CATALOGUE_URL = "http://localhost:3000"

@pytest.fixture
def sample_track():
    return {
        "title": "Blinding Lights",
        "encoded_track": encode_audio_to_base64("./Music/Tracks/Blinding Lights.wav")
    }

#Helper Function
def encode_audio_to_base64(file_path):
    """Reads a WAV file and encodes it to a base64 string."""
    with open(file_path, "rb") as audio_file:
        encoded_string = base64.b64encode(audio_file.read()).decode("utf-8")
    return encoded_string

#Happy Paths
def test_delete_existing_track(sample_track):
    """Test that an existing track can be deleted successfully."""
    # Add the track first
    add_response = requests.post(f"{CATALOGUE_URL}/tracks", json=sample_track)
    assert add_response.status_code == 201

    # Delete the track
    delete_response = requests.delete(f"{CATALOGUE_URL}/tracks/{sample_track['title']}")
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Track deleted successfully"

    # Verify the track is no longer in the catalogue
    tracks_response = requests.get(f"{CATALOGUE_URL}/tracks")
    assert tracks_response.status_code == 200
    tracks = tracks_response.json()
    assert not any(track["title"] == sample_track["title"] for track in tracks)

#Unhappy Paths
def test_delete_nonexistent_track():
    """Test that deleting a non-existent track returns a 404 error."""
    response = requests.delete(f"{CATALOGUE_URL}/tracks/NonExistentTrack")
    assert response.status_code == 404
    assert response.json()["error"] == "Track not found"
