import os
import requests
from flask import Flask, request

KEY  = os.environ["KEY"]
PATH = "https://api.wolframalpha.com/v1/result"

app = Flask(__name__)

@app.route("/alpha",methods=["POST"])
def endpoint():
  js = request.get_json()
  question = js["question"]
  if question != None:
    prms = {"appid":KEY,"i":question}
    rsp = requests.get(f'{PATH}',params=prms)
    if rsp.status_code == 200:
      answer = rsp.text
      return {"answer":answer}, 200 # OK
    else:
      return "",500 # Internal Server Error
  else:
    return "",400 # Bad Request

if __name__ == "__main__":
  app.run(host="localhost",port=3003)