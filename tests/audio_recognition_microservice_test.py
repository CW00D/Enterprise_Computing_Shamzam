import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Ensure the /src directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from audio_recognition_microservice import app

class TestAudioRecognitionMicroservice(unittest.TestCase):
    
    def setUp(self):
        """Set up a test client before each test"""
        self.app = app.test_client()
        self.app.testing = True  # Enable testing mode

    @patch("audio_recognition_microservice.get_track_title_from_api")
    @patch("requests.get")
    def test_recognise_success(self, mock_requests_get, mock_get_track_title):
        """Test successful track recognition and catalogue lookup"""
        mock_get_track_title.return_value = "Blinding Lights"

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"title": "Blinding Lights", "artist": "The Weeknd"}
        mock_requests_get.return_value = mock_response

        response = self.app.post("/recognise", json={"encoded_track_fragment": "base64_audio_data"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"title": "Blinding Lights", "artist": "The Weeknd"})

    @patch("audio_recognition_microservice.get_track_title_from_api")
    def test_recognise_track_not_found(self, mock_get_track_title):
        """Test recognition when track is not found"""
        mock_get_track_title.return_value = "Track not recognised"

        response = self.app.post("/recognise", json={"encoded_track_fragment": "base64_audio_data"})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"error": "Track not recognised"})

    @patch("audio_recognition_microservice.get_track_title_from_api")
    @patch("requests.get")
    def test_recognise_track_not_in_catalogue(self, mock_requests_get, mock_get_track_title):
        """Test when track is recognised but not found in catalogue"""
        mock_get_track_title.return_value = "Blinding Lights"

        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"error": "Track not found"}
        mock_requests_get.return_value = mock_response

        response = self.app.post("/recognise", json={"encoded_track_fragment": "base64_audio_data"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Track not found in catalogue"})

    @patch("audio_recognition_microservice.get_track_title_from_api")
    @patch("requests.get")
    def test_recognise_catalogue_service_error(self, mock_requests_get, mock_get_track_title):
        """Test when the catalogue service fails"""
        mock_get_track_title.return_value = "Blinding Lights"

        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"error": "Internal Server Error"}
        mock_requests_get.return_value = mock_response

        response = self.app.post("/recognise", json={"encoded_track_fragment": "base64_audio_data"})

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"error": "Catalogue service error"})

    def test_recognise_missing_encoded_track(self):
        """Test request with missing encoded_track_fragment"""
        response = self.app.post("/recognise", json={})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Missing encoded_track_fragment"})

if __name__ == "__main__":
    unittest.main()
