import unittest
from unittest.mock import patch
import sys
import os

# Ensure the /src directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from database_management_microservice import app

class TestDatabaseMicroservice(unittest.TestCase):
    
    def setUp(self):
        """Set up a test client before each test"""
        self.app = app.test_client()
        self.app.testing = True  # Enable testing mode

    @patch("database_management_microservice.db.insert")
    def test_add_track_success(self, mock_insert):
        """Test adding a track successfully"""
        mock_insert.return_value = 1  # Simulate database returning track ID 1

        response = self.app.post("/db/tracks", json={
            "title": "Blinding Lights",
            "artist": "The Weeknd",
            "file_path": "/audio/blinding_lights.mp3"
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"id": 1, "message": "Track added successfully"})

    def test_add_track_missing_fields(self):
        """Test adding a track with missing fields"""
        response = self.app.post("/db/tracks", json={"title": "Blinding Lights"})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Missing required fields"})

    @patch("database_management_microservice.db.remove_track_by_id")
    def test_delete_track_success(self, mock_remove):
        """Test deleting a track successfully"""
        mock_remove.return_value = 1  # Simulate one row deleted

        response = self.app.delete("/db/tracks/1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Track deleted successfully"})

    @patch("database_management_microservice.db.remove_track_by_id")
    def test_delete_track_not_found(self, mock_remove):
        """Test deleting a track that does not exist"""
        mock_remove.return_value = 0  # Simulate no rows deleted

        response = self.app.delete("/db/tracks/999")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"error": "Track not found"})

    @patch("database_management_microservice.db.get_all_tracks")
    def test_get_tracks_success(self, mock_get_all):
        """Test getting all tracks successfully"""
        mock_get_all.return_value = [
            {"id": 1, "title": "Blinding Lights", "artist": "The Weeknd", "file_path": "/audio/blinding_lights.mp3"}
        ]

        response = self.app.get("/db/tracks")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [
            {"id": 1, "title": "Blinding Lights", "artist": "The Weeknd", "file_path": "/audio/blinding_lights.mp3"}
        ])

    @patch("database_management_microservice.db.get_all_tracks")
    def test_get_tracks_empty(self, mock_get_all):
        """Test getting tracks when database is empty"""
        mock_get_all.return_value = []  # Simulate empty database

        response = self.app.get("/db/tracks")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])  # Should return an empty list

    @patch("database_management_microservice.db.find_track_by_title_and_artist")
    def test_search_track_success(self, mock_search):
        """Test searching for a track successfully"""
        mock_search.return_value = {
            "id": 1,
            "title": "Blinding Lights",
            "artist": "The Weeknd",
            "file_path": "/audio/blinding_lights.mp3"
        }

        response = self.app.get("/db/tracks/search?title=Blinding Lights&artist=The Weeknd")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "id": 1,
            "title": "Blinding Lights",
            "artist": "The Weeknd",
            "file_path": "/audio/blinding_lights.mp3"
        })

    @patch("database_management_microservice.db.find_track_by_title_and_artist")
    def test_search_track_not_found(self, mock_search):
        """Test searching for a track that does not exist"""
        mock_search.return_value = None  # Simulate track not found

        response = self.app.get("/db/tracks/search?title=Nonexistent&artist=Unknown")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"error": "Track not found"})

if __name__ == "__main__":
    unittest.main()
