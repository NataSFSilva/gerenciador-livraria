from flask import Flask, jsonify, request, make_response
import db
from datetime import datetime

app = Flask(__name__)
app.config['JSONIFY_MIMETYPE'] = 'application/json; charset=utf-8'
app.config['JSON_SORT_KEYS'] = False

def responseGenerator(stts: int, msg: str, dt):
    if dt is None:
        return jsonify(
                status=stts,
                datetime=datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
                message=msg
            ), stts
    
    return jsonify(
                status=stts,
                datetime=datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
                message=msg,
                data=dt
            ), stts

@app.route("/filmes", methods=["GET"])
def getAll():
    filmesList = db.selectAll()

    if len(filmesList) == 0:
        return responseGenerator(204, "Sem conteúdo", None)


    return responseGenerator(200, "Todos os valores", filmesList)


@app.route("/filmes", methods=["POST"])
def postObj():
    novoFilme = request.json
    try:
        db.insert(novoFilme)
        filmes = db.selectAll()
        resgate = filmes[len(filmes) - 1]
        retorno = {
            "id": resgate[0],
            "titulo": resgate[1],
            "genero": resgate[2],
            "direcao": resgate[3],
            "lancamento": resgate[4]
        }

        return responseGenerator(201, "Inserção no banco de dados realizada com sucesso", retorno)
    except Exception as e:
        return responseGenerator(400, str(e), None)

@app.route("/filmes/<int:id>", methods=["GET"])
def getOne(id: int):
    filme = db.selectOne(id)
    
    if filme == None:
        return responseGenerator(404, "Valor não encontrado", None)

    return responseGenerator(200, "Valor encontrado", filme)

app.run(port=5000, host="localhost", debug=True)