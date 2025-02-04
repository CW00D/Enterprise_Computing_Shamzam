import requests
from flask import Flask, request, jsonify
import json

with open("config/credentials.json") as infile:
    json_obj = json.load(infile)
    KEY = json_obj.get("AUDDIO_TOKEN", "")

app = Flask(__name__)
CATALOGUE_URL = "http://localhost:3000"

@app.route("/recognise",methods=["POST"])
def recognise():
    #Handle all the auddio data requesting etc
    title = "Placeholder Title"
    artist = "Placeholder Artist"
    response = requests.get(f"{CATALOGUE_URL}/tracks/search?title={title}&artist={artist}")
    return jsonify(response.json()), response.status_code

if __name__ == "__main__":
    app.run(host="localhost",port=3002)
