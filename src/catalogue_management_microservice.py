import requests
from flask import Flask, request, jsonify
import logging
import os

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Configure logging
logging.basicConfig(filename="logs/catalogue.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = Flask(__name__)
DATABASE_MANAGEMENT_MICROSERVICE_URL = "http://localhost:3001"

# Add a new track
@app.route("/tracks", methods=["POST"])
def add_track():
    data = request.get_json()

    if not data or "title" not in data or "encoded_track" not in data:
        logging.warning("Missing required fields")
        return jsonify({"error": "Missing required fields"}), 400
    
    title = data.get("title", "").strip()  # Strip whitespace
    if not title:  # Check if title is empty after stripping whitespace
        logging.warning("Track title cannot be just whitespace")
        return jsonify({"error": "Track title cannot be just whitespace"}), 400
    
    response = requests.post(f"{DATABASE_MANAGEMENT_MICROSERVICE_URL}/db/tracks", json=data)
    logging.info(response.status_code)
    return jsonify(response.json()), response.status_code

# Delete a track
@app.route("/tracks/<string:title>", methods=["DELETE"])
def delete_track(title):
    if not title.strip():
        logging.warning("Blank track title not valid")
        return jsonify({"error": "Blank track title not valid"}), 400
    response = requests.delete(f"{DATABASE_MANAGEMENT_MICROSERVICE_URL}/db/tracks/{title}")
    return jsonify(response.json()), response.status_code

#Delete with no title to catch error
@app.route("/tracks/", methods=["DELETE"])
def delete_without_title():
    logging.warning("No track title provided")
    return jsonify({"error": "No track title provided"}), 400

# Get all tracks
@app.route("/tracks", methods=["GET"])
def get_tracks():
    response = requests.get(f"{DATABASE_MANAGEMENT_MICROSERVICE_URL}/db/tracks")
    logging.info(response.status_code)
    return jsonify(response.json()), response.status_code

# Get track by title and artist
@app.route("/tracks/search", methods=["GET"])
def search_tracks():
    title = request.args.get("title")
    response = requests.get(f"{DATABASE_MANAGEMENT_MICROSERVICE_URL}/db/tracks/search?title={title}")
    logging.info(response.status_code)
    return jsonify(response.json()), response.status_code

if __name__ == "__main__":
    app.run(host="localhost", port=3000, debug=True)