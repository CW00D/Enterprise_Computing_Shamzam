from flask import Flask, request, jsonify
from database_helper import MusicTrackDatabase

app = Flask(__name__)
db = MusicTrackDatabase()

@app.route("/db/tracks", methods=["POST"])
def add_track():
    data = request.get_json()

    if not data or "title" not in data or "encoded_track" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    track = db.insert(data)
    if track == 409:
        return jsonify({"error": "Attempting to add duplicate track"}), 409
    
    return jsonify({"title": track, "message": "Track added successfully"}), 201

@app.route("/db/tracks/<string:title>", methods=["DELETE"])
def delete_track(title):
    deleted_rows = db.remove_track_by_title(title)

    if deleted_rows == 0:
        return jsonify({"error": "Track not found"}), 404

    return jsonify({"message": "Track deleted successfully"}), 200

@app.route("/db/tracks", methods=["GET"])
def get_tracks():
    tracks = db.get_all_tracks()
    return jsonify(tracks if tracks else []), 200

@app.route("/db/tracks/search", methods=["GET"])
def search_tracks():
    title = request.args.get("title")

    if not title:
        return jsonify({"error": "Missing title query parameters"}), 400

    track = db.find_track_by_title(title)

    if track is None:
        return jsonify({"error": "Track not found"}), 404

    return jsonify(track), 200

if __name__ == "__main__":
    app.run(host="localhost", port=3001, debug=True)
