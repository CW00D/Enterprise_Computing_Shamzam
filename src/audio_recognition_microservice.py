import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the API token
AUDDIO_TOKEN = os.getenv("AUDDIO_TOKEN", "")

if not AUDDIO_TOKEN:
    raise ValueError("AUDDIO_TOKEN is not set in the environment or .env file!")

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
    
    try:
        response = requests.get(f"{CATALOGUE_URL}/tracks/search", params={"title": title})
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return jsonify({"error": "Catalogue service error"}), 500

    if response.status_code == 200:
        return jsonify(response.json()), 200
    elif response.status_code == 404:
        return jsonify({"message": "Track not found in catalogue"}), 200
    else:
        return jsonify({"error": "Unexpected error from catalogue service"}), response.status_code

def get_track_title_from_api(encoded_track_fragment):
    url = "https://api.audd.io/"
    data = {
        "api_token": AUDDIO_TOKEN,
        "audio": encoded_track_fragment,
        "return": "title",
    }
    
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        result = response.json()

        if result.get("status") == "success" and result.get("result"):
            return result["result"]["title"]
        
    except requests.exceptions.RequestException:
        return "Track not recognised"
    
    return "Track not recognised"

if __name__ == "__main__":
    app.run(host="localhost", port=3002)
