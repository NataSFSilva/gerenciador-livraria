from flask import Flask, request
import db
from datetime import datetime

app = Flask(__name__)
app.config['JSONIFY_MIMETYPE'] = 'application/json; charset=utf-8'
app.json.sort_keys = False

def responseSuccess(stts: int, msg: str, dt=None):
    response = {
            'status': stts,
            'datetime': datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            'message': msg
    }

    if dt is not None:
        response['data'] = dt
    
    return response, stts
    
def responseError(stts: int, msg: str):
    response = {
            'status': stts,
            'datetime': datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            'message': msg
    }
    return response, stts

@app.route("/filmes", methods=["GET", "POST"])
def getAll():
    if request.method == "GET":
        filmesList = db.selectAll()

        if len(filmesList) == 0:
            return responseSuccess(204, "Sem conteúdo")
        
        return responseSuccess(200, "Todos os valores", filmesList)
    elif request.method == "POST":
        novoFilme = request.json

        retorno = db.insert(novoFilme)

        return responseSuccess(201, "Inserção no banco de dados realizada com sucesso", retorno)
        
@app.route("/filmes/<int:id>", methods=["GET", "PUT", "DELETE"])
def opsById(id: int):
    if request.method == "GET":
        filme = db.selectById(id)

        if filme == None:
            return responseError(404, "Valor não encontrado")

        return responseSuccess(200, "Valor encontrado", filme)
    elif request.method == "PUT":
        response = db.update(id, request.json)

        if response == False:
            return responseError(400, "Todos os campos são necessários para atualizar")
        
        return responseSuccess(204, "Valor atualizado com sucesso", None)
    elif request.method == "DELETE":
        response = db.delete(id)

        if response == False:
            return responseError(404, "Valor não encontrado")
        
        return responseSuccess(204, "Valor deletado com sucesso", None)

@app.route("/filmes/diretor/<string:d>")
def getByDiretor(d):
    filmes = db.selectByDiretor(d)

    if filmes == None:
        return responseError(404, "Valor não encontrado")
    
    return responseSuccess(200, "Valor encontrado", filmes)

@app.route("/filmes/genero/<string:g>")
def getByGenero(g):
    filmes = db.selectByGenero(g)

    if filmes == None:
        return responseError(404, "Valor não encontrado")
    
    return responseSuccess(200, "Valor encontrado", filmes)

app.run(port=5000, host="localhost", debug=True)