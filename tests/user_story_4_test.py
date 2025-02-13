import requests
import pytest
import base64

CATALOGUE_URL = "http://localhost:3000"
DATABASE_URL = "http://localhost:3001"
AUDIO_RECOGNITION_URL = "http://localhost:3002"

@pytest.fixture
def sample_track():
    return {
        "title": "Don't Look Back In Anger",
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
def test_recognise_valid_fragment(sample_track):
    """Test that a valid track fragment is correctly identified."""
    # Add track to catalogue
    requests.post(f"{CATALOGUE_URL}/tracks", json=sample_track)

    # Simulate recognising a track fragment
    recognition_data = {"encoded_track_fragment": encode_audio_to_base64("./Music/Fragments/_Dont Look Back in Anger.wav")}
    response = requests.post(f"{AUDIO_RECOGNITION_URL}/recognise", json=recognition_data)

    assert response.status_code == 200
    assert response.json().get("title") == sample_track["title"]
    assert response.json().get("encoded_track") == sample_track["encoded_track"]

#Unhappy Paths
def test_recognise_unknown_fragment():
    """Test that an unrecognisable track fragment returns a 400 error."""
    recognition_data = {"encoded_track_fragment": "unknown_base64_fragment"}
    response = requests.post(f"{AUDIO_RECOGNITION_URL}/recognise", json=recognition_data)

    assert response.status_code == 400
    assert response.json().get("error") == "Track not recognised"

def test_recognise_missing_fragment():
    """Test that missing input returns a 400 error."""
    response = requests.post(f"{AUDIO_RECOGNITION_URL}/recognise", json={})

    assert response.status_code == 400
    assert response.json().get("error") == "Missing encoded_track_fragment"

def test_track_not_in_catalogue():
    """Test that a recognised track fragment not in the catalogue returns a 404 error."""
    recognition_data = {"encoded_track_fragment": encode_audio_to_base64("./Music/Fragments/_Dont Look Back in Anger.wav")}
    response = requests.post(f"{AUDIO_RECOGNITION_URL}/recognise", json=recognition_data)

    assert response.status_code == 404
    assert response.json().get("error") == "Track not found in catalogue"