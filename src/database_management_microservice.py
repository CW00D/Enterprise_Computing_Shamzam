import requests
from flask import Flask, request
import json

app = Flask(__name__)

@app.route("/db/tracks",methods=["POST"])
def add_track():
    pass
    #HANDLE 201 (CREATED)
    #HANDLE 400 (BAD REQUEST)

@app.route("/db/tracks/<int:id>",methods=["DELETE"])
def delete_track(id):
    pass
    #HANDLE 200 (OK)
    #HANDLE 404 (NOT FOUND)

@app.route("/db/tracks",methods=["GET"])
def get_tracks():
    pass
    #HANDLE 200 (OK)

@app.route("/db/tracks",methods=["GET"])
def search_tracks():
    pass
    #HANDLE 200 (OK)
    #HANDLE 404 (NOT FOUND)

if __name__ == "__main__":
    app.run(host="localhost",port=3001)
