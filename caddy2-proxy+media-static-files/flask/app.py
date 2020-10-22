from flask import Flask, make_response

app = Flask(__name__)


@app.route("/")
def index():
    response = make_response("hello")
    return response
