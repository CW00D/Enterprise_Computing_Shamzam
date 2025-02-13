from flask import Flask, request, jsonify
import logging
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database_helper import MusicTrackDatabase

# Define log directory within the microservice folder
log_dir = os.path.join(os.path.dirname(__file__))

# Configure logging
logging.basicConfig(filename=os.path.join(log_dir, "database.log"), level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = Flask(__name__)
db = MusicTrackDatabase()

@app.route("/db/tracks", methods=["POST"])
def add_track() -> tuple:
    """
    Adds a new track to the database.

    Returns:
        A JSON response indicating success or failure.
    """
    data = request.get_json()

    if not data or "title" not in data or "encoded_track" not in data:
        logging.warning("Missing required fields")
        return jsonify({"error": "Missing required fields"}), 400

    try:
        track = db.insert(data)
        if track == 409:
            logging.warning("Attempting to add duplicate track")
            return jsonify({"error": "Attempting to add duplicate track"}), 409
        
        logging.info("Track added successfully")
        return jsonify({"title": track, "message": "Track added successfully"}), 201
    except:
        return jsonify({"error": "Database unreachable"}), 503

@app.route("/db/tracks/<string:title>", methods=["DELETE"])
def delete_track(title) -> tuple:
    """
    Deletes a track by title.

    Returns:
        A JSON response indicating success or failure.
    """
    try:
        deleted_rows = db.remove_track_by_title(title)

        if deleted_rows == 0:
            logging.warning("Track not found")
            return jsonify({"error": "Track not found"}), 404

        logging.info("Track deleted successfully")
        return jsonify({"message": "Track deleted successfully"}), 200
    except:
        return jsonify({"error": "Database unreachable"}), 503

@app.route("/db/tracks", methods=["GET"])
def get_tracks() -> tuple:
    """
    Retrieves all tracks from the database.

    Returns:
        A JSON list of tracks.
    """
    try:
        tracks = db.get_all_tracks()
        logging.info("Tracks returned")
        return jsonify(tracks if tracks else []), 200
    except:
        return jsonify({"error": "Database unreachable"}), 503

@app.route("/db/tracks/search", methods=["GET"])
def search_tracks() -> tuple:
    """
    Searches for a track by title.

    Returns:
        A JSON response with the track details or an error.
    """
    title = request.args.get("title")

    if not title:
        logging.warning("Missing title query parameters")
        return jsonify({"error": "Missing title query parameters"}), 400

    try:
        track = db.find_track_by_title(title)

        if track is None:
            logging.warning("Track not found")
            return jsonify({"error": "Track not found"}), 404

        logging.info("Track found")
        return jsonify(track), 200
    except:
        return jsonify({"error": "Database unreachable"}), 503

@app.route("/db/reset", methods=["POST"])
def reset_db() -> tuple:
    """
    Clears all tracks from the database (used for test cleanup only).

    Returns:
        A JSON response indicating success.
    """
    db.reset_database()
    logging.info("Database reset successfully")
    return jsonify({"message": "Database reset successfully"}), 200

if __name__ == "__main__":
    app.run(host="localhost", port=3001, debug=True)
