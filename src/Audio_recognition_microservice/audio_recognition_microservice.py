import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import logging
import os

# Define log directory within the microservice folder
log_dir = os.path.join(os.path.dirname(__file__))

# Configure logging
logging.basicConfig(filename=os.path.join(log_dir, "audio.log"), level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load environment variables from .env file
load_dotenv()

# Retrieve the API token
AUDDIO_TOKEN: str = os.getenv("AUDDIO_TOKEN", "")

if not AUDDIO_TOKEN:
    raise ValueError("AUDDIO_TOKEN is not set in the environment or .env file!")

app = Flask(__name__)
DATABASE_URL = "http://localhost:3002"

@app.route("/recognise", methods=["POST"])
def recognise():
    """
    Recognizes an audio fragment and checks if it exists in the database.

    Returns:
        A JSON response with track details if found, or an error message.
    """
    data = request.json
    encoded_track_fragment = data.get("encoded_track_fragment")

    if not encoded_track_fragment:
        logging.warning("Missing encoded_track_fragment")
        return "", 400

    result = get_track_title_from_api(encoded_track_fragment)

    if not result.get("success"):
        logging.warning(f"API error: {result.get('error_message')}")
        return "", result.get("error_code")
    
    title = result.get("title")

    response = requests.get(f"{DATABASE_URL}/db/tracks/search", params={"title": title})
    if response.status_code == 200:
        logging.info("Track found in database")
        return jsonify(response.json()), 200
    elif response.status_code == 404:
        logging.info("Track not found in database")
        return "", 404
    else:
        logging.warning("Unexpected error from database service")
        return "", response.status_code

def get_track_title_from_api(encoded_track_fragment: str):
    """
    Calls the external AudD.io API to recognize the track title.

    Returns:
        dict: On success, returns {"success": True, "title": <track title>}.
              On failure, returns {"success": False, "error_code": <HTTP code>, "error_message": <description>}.
    """
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
            return {"success": True, "title": result["result"]["title"]}
        elif result.get("status") == "error":
            error_info = result.get("error", {})
            error_code = error_info.get("error_code", "#100")
            error_message = error_info.get("error_message", "An unknown error occurred.")
            error_mapping = {
                902: 401,  # API limit reached 
                901: 401,  # No api_token passed
                900: 401,  # Wrong API token.
                600: 400,  # Incorrect audio URL.
                700: 400,  # No file sent for recognition.
                500: 422,  # Incorrect audio file.
                400: 413,  # Too big audio file.
                300: 422,  # Fingerprinting error.
                100: 500   # Unknown error.
            }
            http_status = error_mapping.get(error_code, 500)
            logging.warning(error_message)
            return {"success": False, "error_code": http_status, "error_message": "AUDD.io API Error"}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error_code": 500, "error_message": f"External API request failed: {str(e)}"}
    
    # Fallback error:
    return {"success": False, "error_code": 500, "error_message": "Track not recognised"}

if __name__ == "__main__":
    app.run(host="localhost", port=3001, debug=True)
