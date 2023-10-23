from flask import Flask, jsonify, request
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

@app.route("/filmes", methods=["GET", "POST"])
def getAll():
    if request.method == "GET":
        filmesList = db.selectAll()

        if len(filmesList) == 0:
            return responseGenerator(204, "Sem conteúdo", None)


        return responseGenerator(200, "Todos os valores", filmesList)
    elif request.method == "POST":
        novoFilme = request.json
        retorno = db.insert(novoFilme)
        return responseGenerator(201, "Inserção no banco de dados realizada com sucesso", retorno)
        # try:
        # except Exception as e:
        #     return responseGenerator(400, e, None)
        
@app.route("/filmes/<int:id>", methods=["GET"])
def getOne(id: int):
    filme = db.selectOne(id)
    
    if filme == None:
        return responseGenerator(404, "Valor não encontrado", filme)

    return responseGenerator(200, "Valor encontrado", filme)

@app.route("/filmes/<string:d>")
def getByDiretor(d):
    filmes = db.selectByDiretor(d)

    if filmes == None:
        return responseGenerator(404, "Valor não encontrado", filmes)
    
    return responseGenerator(200, "Valor encontrado", filmes)

@app.route("/filmes/<string:g>")
def getByGenero(g):
    filmes = db.selectByGenero(g)

    if filmes == None:
        return responseGenerator(404, "Valor não encontrado", filmes)
    
    return responseGenerator(200, "Valor encontrado", filmes)

app.run(port=5000, host="localhost", debug=True)