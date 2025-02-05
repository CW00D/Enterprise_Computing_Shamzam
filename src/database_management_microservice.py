from flask import Flask, request, jsonify
from database_helper import MusicTrackDatabase

app = Flask(__name__)
db = MusicTrackDatabase()

@app.route("/db/tracks", methods=["POST"])
def add_track():
    data = request.get_json()

    if not data or "title" not in data or "artist" not in data or "file_path" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    track_id = db.insert(data)
    return jsonify({"id": track_id, "message": "Track added successfully"}), 201

@app.route("/db/tracks/<int:id>", methods=["DELETE"])
def delete_track(id):
    deleted_rows = db.remove_track_by_id(id)

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
    artist = request.args.get("artist")

    if not title or not artist:
        return jsonify({"error": "Missing title or artist query parameters"}), 400

    track = db.find_track_by_title_and_artist(title, artist)

    if track is None:
        return jsonify({"error": "Track not found"}), 404

    return jsonify(track), 200

if __name__ == "__main__":
    app.run(host="localhost", port=3001, debug=True)
