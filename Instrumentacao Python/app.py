from flask import Flask, request
import db
from datetime import datetime
import json
# from flask_restplus import Api
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
    logging.info("Function getPost() called")
    if request.method == "GET":
        logging.info("GET request in the endpoint /filmes")

        filmesList = db.selectAll()

        if len(filmesList) == 0:
            logging.info("Database query returned empty content")
            return responseSuccess(204, "No content")
        
        logging.debug("Data: " + str(filmesList))
        logging.info("Success query")
        return responseSuccess(200, "Success request", filmesList)
    
    elif request.method == "POST":
        logging.info("POST request in the endpoint /filmes")
        novoFilme = request.json

        if novoFilme['titulo'] == None or novoFilme['direcao'] == None or novoFilme['genero'] == None or novoFilme['lancamento'] == None:
            logging.warning("Mandatory data not provided")
            return responseError(400, "Bad request")

        retorno = db.insert(novoFilme)

        logging.debug("Data: " + json.dumps(retorno))
        logging.info("Data added to the database")
        return responseSuccess(201, "Successful database insertion", retorno)
        
@app.route("/filmes/<int:id>", methods=["GET", "PUT", "DELETE"])
def opsById(id: int):
    logging.info("Function opsById() called")
    if request.method == "GET":
        logging.info("GET request in the endpoint /filmes/<int:id>")
        filme = db.selectById(id)

        if filme == None:
            logging.warning("Data not found")
            return responseError(404, "Value not found")

        logging.debug("Data: " + json.dumps(filme))
        logging.info("Found value")
        return responseSuccess(200, "Success request", filme)
    elif request.method == "PUT":
        logging.info("PUT request in the endpoint /filmes/<int:id>")
        response = db.update(id, request.json)

        if response == False:
            logging.warning("Mandatory data not provided")
            return responseError(400, "Bad request")
        
        logging.info(f"Data of ID {id} updated")
        return responseSuccess(204, "Value updated successfully")
    elif request.method == "DELETE":
        logging.info("DELETE request in the endpoint /filmes/<int:id>")
        response = db.delete(id)

        if response == False:
            logging.warning("Data not found")
            return responseError(404, "Value not found")
        
        logging.info(f"Data of ID {id} deleted")
        return responseSuccess(204, "Value deleted successfully", None)

@app.route("/filmes/diretor/<string:d>", methods=["GET"])
def getByDiretor(d):
    logging.info("Function getByDiretor() called")
    logging.info("GET request in the endpoint /filmes/diretor/<string:d>")
    filmes = db.selectByDiretor(d)

    if filmes == None:
        logging.warning("Data not found")
        return responseError(404, "Value not found")
    
    logging.debug("Data: " + str(filmes))
    logging.info("Found value")
    return responseSuccess(200, "Success request", filmes)

@app.route("/filmes/genero/<string:g>", methods=["GET"])
def getByGenero(g):
    logging.info("Function getByGenero() called")
    logging.info("GET request in the endpoint /filmes/genero/<string:g>")
    filmes = db.selectByGenero(g)

    if filmes == None:
        logging.warning("Data not found")
        return responseError(404, "Value not found")
    
    logging.debug("Data: " + str(filmes))
    logging.info("Success request")
    return responseSuccess(200, "Found value with sucess", filmes)

app.run(port=5000, host="localhost", debug=True)