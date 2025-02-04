import requests
from flask import Flask, request, jsonify

app = Flask(__name__)
DATABASE_URL = "http://localhost:3001"

# Add a new track
@app.route("/tracks", methods=["POST"])
def add_track():
    data = request.get_json()
    if not data or "title" not in data or "artist" not in data or "file_path" not in data:
        return jsonify({"error": "Missing required fields"}), 400
    response = requests.post(f"{DATABASE_URL}/db/tracks", json=data)
    return jsonify(response.json()), response.status_code

# Delete a track
@app.route("/tracks/<int:id>", methods=["DELETE"])
def delete_track(id):
    response = requests.delete(f"{DATABASE_URL}/db/tracks/{id}")
    return jsonify(response.json()), response.status_code

# Get all tracks
@app.route("/tracks", methods=["GET"])
def get_tracks():
    response = requests.get(f"{DATABASE_URL}/db/tracks")
    return jsonify(response.json()), response.status_code

# Get track by title and artist
@app.route("/tracks/search", methods=["GET"])
def search_tracks():
    title = request.args.get("title")
    artist = request.args.get("artist")
    response = requests.get(f"{DATABASE_URL}/db/tracks/search?title={title}&artist={artist}")
    return jsonify(response.json()), response.status_code

if __name__ == "__main__":
    app.run(host="localhost", port=3000, debug=True)