import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import logging
import os

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Configure logging
logging.basicConfig(filename="logs/audio.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

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
        logging.warning("Missing encoded_track_fragment")
        return jsonify({"error": "Missing encoded_track_fragment"}), 400

    title = get_track_title_from_api(encoded_track_fragment)

    if title == "Track not recognised":
        logging.warning("Track not recognised")
        return jsonify({"error": "Track not recognised"}), 404

    response = requests.get(f"{CATALOGUE_URL}/tracks/search", params={"title": title})
    if response.status_code == 200:
        logging.info("Track found in catalogue")
        return jsonify(response.json()), 200
    elif response.status_code == 404:
        print("Track not found in catalogue")
        logging.info("Track not found in catalogue")
        return jsonify({"error": "Track not found in catalogue"}), 404
    else:
        logging.warning("Unexpected error from catalogue service")
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
