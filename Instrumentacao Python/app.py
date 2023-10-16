from flask import Flask, jsonify, request
from filme import Filme

app = Flask(__name__)
filmes = [
    Filme(),
]

@app.route("/")
def hello_world( ):
    return "<p>Hello World!</p>"
