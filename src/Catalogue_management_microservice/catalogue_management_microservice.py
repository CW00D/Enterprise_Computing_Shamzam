import requests
from flask import Flask, request, jsonify
import logging
import os

# Define log directory within the microservice folder
log_dir = os.path.join(os.path.dirname(__file__))

# Configure logging
logging.basicConfig(filename=os.path.join(log_dir, "catalogue.log"), level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = Flask(__name__)
DATABASE_MANAGEMENT_MICROSERVICE_URL = "http://localhost:3001"

# Add a new track
@app.route("/tracks", methods=["POST"])
def add_track():
    """
    Adds a new track to the database.

    Returns:
        A JSON response with the track addition status.
    """

    if not request.is_json:
        logging.warning("No json content type")
        return "", 415

    data = request.get_json()
    if not data or "title" not in data or "encoded_track" not in data:
        logging.warning("Missing required fields")
        return jsonify({"error": "Missing required fields"}), 400

    #ADD CHECK FOR ENDCODED TRACK DECODING INTO A .WAV
    
    response = requests.post(f"{DATABASE_MANAGEMENT_MICROSERVICE_URL}/db/tracks", json=data)
    return "", response.status_code

# Delete a track
@app.route("/tracks/<string:title>", methods=["DELETE"])
def delete_track(title: str):
    """
    Deletes a track by title.

    Returns:
        A JSON response with the deletion status.
    """

    if type(title) != str:
        logging.warning("Title provided wasnt a string")
        return "", 415

    response = requests.delete(f"{DATABASE_MANAGEMENT_MICROSERVICE_URL}/db/tracks/{title}")
    return "", response.status_code

# Delete with no title to catch error
@app.route("/tracks/", methods=["DELETE"])
def delete_without_title():
    """
    Handles a request to delete a track without providing a title.

    Returns:
        A JSON error response.
    """
    logging.warning("No track title provided")
    return "", 400

# Get all tracks
@app.route("/tracks", methods=["GET"])
def get_tracks():
    """
    Retrieves all tracks from the database.

    Returns:
        A JSON list of tracks.
    """
    response = requests.get(f"{DATABASE_MANAGEMENT_MICROSERVICE_URL}/db/tracks")
    return "", response.status_code

# Get track by title and artist
@app.route("/tracks/search", methods=["GET"])
def search_tracks():
    """
    Searches for a track by title.

    Returns:
        A JSON response with the track details or an error.
    """
    title = request.args.get("title")
    response = requests.get(f"{DATABASE_MANAGEMENT_MICROSERVICE_URL}/db/tracks/search?title={title}")
    return "", response.status_code

if __name__ == "__main__":
    app.run(host="localhost", port=3000, debug=True)