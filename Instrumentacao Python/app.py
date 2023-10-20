from flask import Flask, jsonify, request, make_response
from db import Filmes, insert
from datetime import datetime

app = Flask(__name__)
app.config['JSONIFY_MIMETYPE'] = 'application/json; charset=utf-8'
app.config['JSON_SORT_KEYS'] = False


@app.route("/filmes", methods=["GET"])
def getAll():
    if len(Filmes) == 0:
        return jsonify(
            status=204,
            datetime=datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            message="Sem conteúdo"
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
        insert(novoFilme)
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
            datetime=datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            error=str(e)
        ), 400

@app.route("/filmes/<int:id>", methods=["GET"])
def getOne(id: int):
    if len(Filmes) == 0:
        return jsonify(
            status=204,
            datetime=datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            message="Sem conteúdo"
        ), 204

    for filme in Filmes:
        if filme['id'] == id:
            return jsonify(
            status=200,
            datetime=datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            message="Valor encontrado",
            data=filme
        ), 200
    
    return jsonify(
            status=404,
            datetime=datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            message="Valor não encontrado"
        ), 404 

app.run(port=5000, host="localhost", debug=True)
