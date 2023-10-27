from flask import Flask, request
import db
from datetime import datetime
import logging
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

resource = Resource.create({SERVICE_NAME: "flask-jornada"})
trace.set_tracer_provider(TracerProvider(resource=resource))

otlp_exporter = OTLPSpanExporter(
    endpoint="http://localhost:4318",
    headers={},
)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

app = Flask(__name__)
app.config['JSONIFY_MIMETYPE'] = 'application/json; charset=utf-8'
app.json.sort_keys = False

logging.basicConfig(level=logging.INFO, filename="aplicacao.log", format="%(asctime)s - %(levelname)s %(message)s")
logging.getLogger().setLevel(logging.DEBUG)

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
def getPost():
    logging.info("Função getPost() foi chamada")
    if request.method == "GET":
        logging.info("Requisição com verbo GET no endpoint /filmes")

        filmesList = db.selectAll()

        if len(filmesList) == 0:
            logging.info("Consulta no banco retornou conteúdo vazio")
            return responseSuccess(204, "Sem conteúdo")
        
        logging.info("Consulta sucedida")
        return responseSuccess(200, "Todos os valores", filmesList)
    
    elif request.method == "POST":
        logging.info("Requisição com verbo POST no endpoint /filmes")
        novoFilme = request.json

        if novoFilme['titulo'] == None or novoFilme['direcao'] == None or novoFilme['genero'] == None or novoFilme['lancamento'] == None:
            logging.error("Falta de informações necessárias no corpo da requisição")
            return responseError(400, "Dados necessários não identificados no corpo da requisição")

        retorno = db.insert(novoFilme)

        logging.info("Filme adicionado no banco de dados")
        return responseSuccess(201, "Inserção no banco de dados realizada com sucesso", retorno)
        
@app.route("/filmes/<int:id>", methods=["GET", "PUT", "DELETE"])
def opsById(id: int):
    logging.info("Função opsById() chamada")
    if request.method == "GET":
        logging.info("Requisição com verbo GET no endpoint /filmes/<int:id>")
        filme = db.selectById(id)

        if filme == None:
            logging.error("Nenhum dado bate com a request")
            return responseError(404, "Valor não encontrado")

        return responseSuccess(200, "Valor encontrado", filme)
    elif request.method == "PUT":
        logging.info("Requisição com verbo PUT no endpoint /filmes/<int:id>")
        response = db.update(id, request.json)

        if response == False:
            logging.error("Requisição passada com elementos errados")
            return responseError(400, "Todos os campos são necessários para atualizar")
        
        logging.info(f"Dado do ID {id} atualizado")
        return responseSuccess(204, "Valor atualizado com sucesso", None)
    elif request.method == "DELETE":
        logging.info("Requisição com verbo DELETE no endpoint /filmes/<int:id>")
        response = db.delete(id)

        if response == False:
            logging.error("Nenhum dado bate com a request")
            return responseError(404, "Valor não encontrado")
        
        logging.info(f"Delete do dado de ID {id} realizado")
        return responseSuccess(204, "Valor deletado com sucesso", None)

@app.route("/filmes/diretor/<string:d>", methods=["GET"])
def getByDiretor(d):
    logging.info("Função getByDiretor() chamada")
    logging.info("Requisição com verbo GET no endpoint /filmes/diretor/<string:d>")
    filmes = db.selectByDiretor(d)

    if filmes == None:
        logging.error("Nenhum dado bate com a request")
        return responseError(404, "Valor não encontrado")
    
    logging.info("Consulta bem sucedida")
    return responseSuccess(200, "Valor encontrado", filmes)

@app.route("/filmes/genero/<string:g>", methods=["GET"])
def getByGenero(g):
    logging.info("Função getByGenero() chamada")
    logging.info("Requisição com verbo GET no endpoint /filmes/genero/<string:g>")
    filmes = db.selectByGenero(g)

    if filmes == None:
        logging.error("Nenhum dado bate com a request")
        return responseError(404, "Valor não encontrado")
    
    logging.info("Consulta bem sucedida")
    return responseSuccess(200, "Valor encontrado", filmes)

app.run(port=5000, host="localhost", debug=True)