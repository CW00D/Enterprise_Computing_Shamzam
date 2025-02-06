import requests
from flask import Flask, request, jsonify
import json

# Load API token from credentials file
with open("config/credentials.json") as infile:
    json_obj = json.load(infile)
    AUDDIO_TOKEN = json_obj.get("AUDDIO_TOKEN", "")

app = Flask(__name__)
CATALOGUE_URL = "http://localhost:3000"

@app.route("/recognise", methods=["POST"])
def recognise():
    data = request.json
    encoded_track_fragment = data.get("encoded_track_fragment")

    if not encoded_track_fragment:
        return jsonify({"error": "Missing encoded_track_fragment"}), 400

    title = get_track_title_from_api(encoded_track_fragment)

    if title == "Track not recognised":
        return jsonify({"error": "Track not recognised"}), 404
    
    print(title)
    response = requests.get(f"{CATALOGUE_URL}/tracks/search", params={"title": title})

    if response.status_code == 200:
        return jsonify(response.json()), 200
    elif response.status_code == 404:
        return jsonify({"message": "Track not found in catalogue"}), 200
    else:
        return jsonify({"error": "Catalogue service error"}), response.status_code


def get_track_title_from_api(encoded_track_fragment):
    url = "https://api.audd.io/"
    data = {
        "api_token": AUDDIO_TOKEN,
        "audio": encoded_track_fragment,
        "return": "title",
    }
    
    response = requests.post(url, data=data)

    if response.status_code == 200:
        result = response.json()
        if result.get("status") == "success" and result.get("result"):
            return result["result"]["title"]
    
    return "Track not recognised"

if __name__ == "__main__":
    app.run(host="localhost", port=3002)
