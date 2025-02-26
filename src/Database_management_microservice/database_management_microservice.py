from flask import Flask, request, jsonify
import logging
import os
import sys
from database_helper import MusicTrackDatabase

# Define log directory within the microservice folder
log_dir = os.path.join(os.path.dirname(__file__))

# Configure logging
logging.basicConfig(filename=os.path.join(log_dir, "database.log"), level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = Flask(__name__)
db = MusicTrackDatabase()

@app.route("/db/tracks", methods=["POST"])
def add_track():
    """
    Adds a new track to the database.

    Returns:
        A JSON response indicating success or failure.
    """
    if not request.is_json:
        logging.warning("No json content type")
        return "", 415
    
    data = request.get_json()

    if not data or "title" not in data or "encoded_track" not in data:
        logging.warning("Missing required fields")
        return jsonify({"error": "Missing required fields"}), 400

    try:
        track = db.insert(data)
        if track == 409:
            logging.warning("Attempting to add duplicate track")
            return "", 409
        
        logging.info("Track added successfully")
        return jsonify({"title": track, "message": "Track added successfully"}), 201
    except:
        logging.warning("Database unreachable")
        return "", 503

@app.route("/db/tracks/<string:title>", methods=["DELETE"])
def delete_track(title):
    """
    Deletes a track by title.

    Returns:
        A JSON response indicating success or failure.
    """
    try:
        deleted_rows = db.remove_track_by_title(title)

        if deleted_rows == 0:
            logging.warning("Track not found")
            return "", 404

        logging.info("Track deleted successfully")
        return jsonify({"message": "Track deleted successfully"}), 200
    except:
        logging.warning("Databse unreachable")
        return "", 503

@app.route("/db/tracks", methods=["GET"])
def get_tracks():
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
        logging.warning("Databse unreachable")
        return "", 503

@app.route("/db/tracks/search", methods=["GET"])
def search_tracks():
    """
    Searches for a track by title.

    Returns:
        A JSON response with the track details or an error.
    """  
    title = request.args.get("title")

    if not title:
        logging.warning("Missing title query parameters")
        return "", 400

    try:
        track = db.find_track_by_title(title)

        if track is None:
            logging.warning("Track not found")
            return "", 404

        logging.info("Track found")
        return jsonify(track), 200
    except:
        logging.warning("Database unreachable")
        return "", 503

@app.route("/db/reset", methods=["POST"])
def reset_db():
    """
    Clears all tracks from the database (used for test cleanup only).

    Returns:
        A JSON response indicating success.
    """
    db.reset_database()
    logging.info("Database reset successfully")
    return jsonify({"message": "Database reset successfully"}), 200

if __name__ == "__main__":
    app.run(host="localhost", port=3002, debug=True)
