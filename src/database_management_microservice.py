from flask import Flask, request, jsonify
from database_helper import MusicTrackDatabase
import logging
import os

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Configure logging
logging.basicConfig(filename="logs/database.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = Flask(__name__)
db = MusicTrackDatabase()

@app.route("/db/tracks", methods=["POST"])
def add_track():
    data = request.get_json()

    if not data or "title" not in data or "encoded_track" not in data:
        logging.warning("Missing required fields")
        return jsonify({"error": "Missing required fields"}), 400

    track = db.insert(data)
    if track == 409:
        logging.warning("Attempting to add duplicate track")
        return jsonify({"error": "Attempting to add duplicate track"}), 409
    
    logging.info("Track added successfully")
    return jsonify({"title": track, "message": "Track added successfully"}), 201

@app.route("/db/tracks/<string:title>", methods=["DELETE"])
def delete_track(title):
    deleted_rows = db.remove_track_by_title(title)

    if deleted_rows == 0:
        logging.warning("Track not found")
        return jsonify({"error": "Track not found"}), 404

    logging.info("Track deleted successfully")
    return jsonify({"message": "Track deleted successfully"}), 200

@app.route("/db/tracks", methods=["GET"])
def get_tracks():
    tracks = db.get_all_tracks()
    logging.info("Tracks returned")
    return jsonify(tracks if tracks else []), 200

@app.route("/db/tracks/search", methods=["GET"])
def search_tracks():
    title = request.args.get("title")

    if not title:
        logging.warning("Missing title query parameters")
        return jsonify({"error": "Missing title query parameters"}), 400

    track = db.find_track_by_title(title)

    if track is None:
        logging.warning("Track not found")
        return jsonify({"error": "Track not found"}), 404

    logging.info("Track found")
    return jsonify(track), 200

@app.route("/db/reset", methods=["POST"])
def reset_db():
    """Clears all tracks from the database (test cleanup)."""
    db.reset_database()
    logging.info("Database reset successfully")
    return jsonify({"message": "Database reset successfully"}), 200

if __name__ == "__main__":
    app.run(host="localhost", port=3001, debug=True)
