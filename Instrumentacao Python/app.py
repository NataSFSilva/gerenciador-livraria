from flask import Flask, jsonify, request, make_response
from db import Filmes, insert

app = Flask(__name__)
app.config['JSON_SORT-KEYS'] = False


@app.route("/filmes", methods=["GET"])
def getAll():
    return make_response(
        jsonify(Filmes),
        200
    )


@app.route("/filmes", methods=["POST"])
def postObj():
    novoFilme = request.json
    try:
        filme_inserido = insert(novoFilme)
        return jsonify(
            status=201,
            mensagem='Inserção no pseudo-database',
            data=filme_inserido
        ), 201
    except Exception as e:
        return jsonify(
            status=400,
            error=str(e)
        ), 400


app.run(port=5000, host="localhost", debug=True)