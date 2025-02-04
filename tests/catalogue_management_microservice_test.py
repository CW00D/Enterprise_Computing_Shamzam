import unittest
from unittest.mock import patch
import sys
import os

# Ensure the /src directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from catalogue_management_microservice import app

class TestCatalogueMicroservice(unittest.TestCase):
    
    def setUp(self):
        """Set up a test client before each test"""
        self.app = app.test_client()
        self.app.testing = True  # Enable testing mode

    @patch("requests.post")
    def test_add_track_success(self, mock_post):
        """Test adding a track successfully"""
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = {"id": 1, "message": "Track added successfully"}

        response = self.app.post("/tracks", json={
            "title": "Blinding Lights",
            "artist": "The Weeknd",
            "file_path": "/audio/blinding_lights.mp3"
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"id": 1, "message": "Track added successfully"})

    @patch("requests.post")
    def test_add_track_missing_fields(self, mock_post):
        """Test adding a track with missing fields"""
        response = self.app.post("/tracks", json={"title": "Blinding Lights"})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Missing required fields"})

    @patch("requests.delete")
    def test_delete_track_success(self, mock_delete):
        """Test deleting a track successfully"""
        mock_delete.return_value.status_code = 200
        mock_delete.return_value.json.return_value = {"message": "Track deleted successfully"}

        response = self.app.delete("/tracks/1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Track deleted successfully"})

    @patch("requests.delete")
    def test_delete_track_not_found(self, mock_delete):
        """Test deleting a track that does not exist"""
        mock_delete.return_value.status_code = 404
        mock_delete.return_value.json.return_value = {"error": "Track not found"}

        response = self.app.delete("/tracks/999")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"error": "Track not found"})

    @patch("requests.get")
    def test_get_tracks_success(self, mock_get):
        """Test getting all tracks successfully"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {"id": 1, "title": "Blinding Lights", "artist": "The Weeknd", "file_path": "/audio/blinding_lights.mp3"}
        ]

        response = self.app.get("/tracks")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [
            {"id": 1, "title": "Blinding Lights", "artist": "The Weeknd", "file_path": "/audio/blinding_lights.mp3"}
        ])

    @patch("requests.get")
    def test_search_track_success(self, mock_get):
        """Test searching for a track successfully"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "id": 1,
            "title": "Blinding Lights",
            "artist": "The Weeknd",
            "file_path": "/audio/blinding_lights.mp3"
        }

        response = self.app.get("/tracks/search?title=Blinding Lights&artist=The Weeknd")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "id": 1,
            "title": "Blinding Lights",
            "artist": "The Weeknd",
            "file_path": "/audio/blinding_lights.mp3"
        })

    @patch("requests.get")
    def test_search_track_not_found(self, mock_get):
        """Test searching for a track that does not exist"""
        mock_get.return_value.status_code = 404
        mock_get.return_value.json.return_value = {"error": "Track not found"}

        response = self.app.get("/tracks/search?title=Nonexistent&artist=Unknown")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"error": "Track not found"})

if __name__ == "__main__":
    unittest.main()
