import requests
from flask import Flask, request
import json

with open("config/credentials.json") as infile:
    json_obj = json.load(infile)
    KEY = json_obj.get("AUDDIO_TOKEN", "")

app = Flask(__name__)

@app.route("/recognise",methods=["POST"])
def recognise():
    pass
    #HANDLE 200 (OK)
    #HANDLE 400 (BAD REQUEST)

if __name__ == "__main__":
    app.run(host="localhost",port=3002)
