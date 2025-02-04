import requests
from flask import Flask, request, jsonify

app = Flask(__name__)
DATABASE_URL = "http://localhost:3001"

# Add a new track
@app.route("/tracks", methods=["POST"])
def add_track():
    pass
    #HANDLE 201 (CREATED)
    #HANDLE 400 (BAD REQUEST)

# Delete a track
@app.route("/tracks/<int:id>", methods=["DELETE"])
def delete_track(id):
    pass
    #HANDLE 200 (OK)
    #HANDLE 404 (NOT FOUND)

# Get all tracks
@app.route("/tracks", methods=["GET"])
def get_tracks():
    pass
    #HANDLE 200 (OK)

# Get track by title and artist
@app.route("/tracks/search", methods=["GET"])
def search_tracks():
    title = request.args.get("title")
    artist = request.args.get("artist")
    print(title)
    print(artist)
    pass
    #HANDLE 200 (OK)
    #HANDLE 404 (NOT FOUND)

if __name__ == "__main__":
    app.run(host="localhost", port=3000, debug=True)