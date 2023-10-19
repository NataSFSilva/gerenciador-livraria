from flask import Flask, jsonify, request, make_response
from db import Filmes, insert
from datetime import datetime

app = Flask(__name__)
app.config['JSON_SORT-KEYS'] = False


@app.route("/filmes", methods=["GET"])
def getAll():
    if len(Filmes) == 0:
        return jsonify(
            status=204,
            datetime=datetime.today(),
            message="No content"
        ), 204

    return make_response(
        jsonify(
            status=200,
            datetime=datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            data=Filmes
        ), 200
    )


@app.route("/filmes", methods=["POST"])
def postObj():
    novoFilme = request.json
    try:
        filme_inserido = insert(novoFilme)
        resgate = Filmes[len(Filmes) - 1]
        retorno = {
            "id": resgate.id,
            "titulo": resgate.titulo,
            "genero": resgate.genero,
            "direcao": resgate.direcao,
            "lancamento": resgate.lancamento
        }

        return jsonify(
            status=201,
            datetime=datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            message="Inserção no pseudo-database",
            data=retorno
        ), 201
    except Exception as e:
        return jsonify(
            status=400,
            error=str(e)
        ), 400


app.run(port=5000, host="localhost", debug=True)
