import requests
import pytest
import base64

CATALOGUE_URL = "http://localhost:3000"

@pytest.fixture
def sample_track():
    return {
        "title": "Dont Look Back in Anger",
        "encoded_track": encode_audio_to_base64("./Music/Tracks/Dont Look Back in Anger.wav")
    }

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
    assert response.json()["message"] == "Track added successfully"

    # Verify the track is in the catalogue
    tracks_response = requests.get(f"{CATALOGUE_URL}/tracks")
    assert tracks_response.status_code == 200
    tracks = tracks_response.json()
    assert any(track["title"] == sample_track["title"] for track in tracks)

#Unhappy Paths
def test_add_track_missing_fields():
    """Test that adding a track with missing fields returns a 400 error."""
    incomplete_track = {"title": "Incomplete Song"}  # Missing encoded_track
    response = requests.post(f"{CATALOGUE_URL}/tracks", json=incomplete_track)
    assert response.status_code == 400
    assert "error" in response.json()

def test_duplicate_track(sample_track):
    """Test that adding the same track twice is handled correctly."""
    # Add the track once
    requests.post(f"{CATALOGUE_URL}/tracks", json=sample_track)

    # Attempt to add the same track again
    response = requests.post(f"{CATALOGUE_URL}/tracks", json=sample_track)
    
    # Depending on implementation, it might return 409 Conflict or allow duplicates
    assert response.status_code == 409