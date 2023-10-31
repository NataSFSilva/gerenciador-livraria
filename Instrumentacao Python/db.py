import mysql.connector
from datetime import date
import logging
logging.basicConfig(filename="aplicacao.log", format="%(asctime)s -  %(levelname)s %(message)s")

mydb = mysql.connector.connect(
    host='localhost',
    port=3306,
    user='root',
    password='prvzcpy',
    database='Streaming'
)

def selectAll():
    logging.info("Function selectAll() was called")
    cursorOps = mydb.cursor()
    cursorOps.execute('SELECT * FROM filme')
    filmes = list()

    for filme in cursorOps.fetchall():
        filmes.append(
            {
                "id": filme[0],
                "titulo": filme[1],
                "direcao": filme[2],
                "genero": filme[3],
                "lancamento": filme[4].strftime("%Y-%m-%d")
            }
        )

    logging.info("All selected data")

    return filmes

def selectById(id):
    logging.info("Function selectById() was called")
    cursorOps = mydb.cursor()
    cursorOps.execute(f"SELECT * FROM filme WHERE id = {id}")
    filme = cursorOps.fetchall()

    if len(filme) == 0:
        logging.warning(f"ID {id} value not found")
        return None
    
    logging.info(f"ID {id} film has been found")
    f = filme[0]
    return {
        "id": f[0],
        "titulo": f[1],
        "direcao": f[2],
        "genero": f[3],
        "lancamento": f[4].strftime("%Y-%m-%d")
    }

def insert(valores):
    logging.info("Function insert() was called")
    logging.info("Insertion into the database")
    cursorOps = mydb.cursor()
    cursorOps.execute(f"INSERT INTO filme (titulo, genero, direcao, lancamento) VALUES ('{valores['titulo']}', '{valores['genero']}', '{valores['direcao']}', '{date.fromisoformat(valores['lancamento']).strftime('%Y-%m-%d')}')")
    mydb.commit()

    logging.info("Verifying inserted data")
    filmes = selectAll()
    novo = filmes[len(filmes) - 1]

    return novo

def selectByDiretor(d):
    logging.info("Function selectByDiretor() was called")
    cursorOps = mydb.cursor()
    cursorOps.execute(f"SELECT * FROM filme WHERE direcao='{d}'")
    filmes = cursorOps.fetchall()

    if len(filmes) == 0:
        logging.warning(f"No films directed by {d} were found")
        return None
    
    retorno = list()

    for f in filmes:
        retorno.append(
            {
                "id": f[0],
                "titulo": f[1],
                "direcao": f[2],
                "genero": f[3],
                "lancamento": f[4].strftime("%Y-%m-%d")
            }
        )
    
    return retorno

def selectByGenero(g):
    logging.info("Function selectByGenero() was called")
    cursorOps = mydb.cursor()
    cursorOps.execute(f"SELECT * FROM filme WHERE genero LIKE '%{g}%'")
    filmes = cursorOps.fetchall()

    if len(filmes) == 0:
        logging.warning(f"No films  of the {g} genre were found")
        return None
    
    retorno = list()

    for f in filmes:
        retorno.append(
            {
                "id": f[0],
                "titulo": f[1],
                "direcao": f[2],
                "genero": f[3],
                "lancamento": f[4].strftime("%Y-%m-%d")
            }
        )
    
    return retorno

def update(id: int, body):
    logging.info("Function update() was called")
    if (body['titulo'] == None or body['direcao'] == None or body['genero'] == None or body['lancamento'] == None) or selectById(id) == None:
        logging.debug("Request body: " + body)
        return False
    
    comando = f"UPDATE filme SET titulo = '{body['titulo']}', direcao = '{body['direcao']}', genero = '{body['genero']}', lancamento = '{body['lancamento']}' WHERE id = {id}"
    cursorOps = mydb.cursor()
    cursorOps.execute(comando)
    mydb.commit()

    return True;

def delete(id: int):
    logging.info("Function delete() was called")
    if selectById(id) == None:
        logging.debug("Provided ID is null, returning false")
        return False

    cursorOps = mydb.cursor()
    cursorOps.execute(f"DELETE FROM filme WHERE id={id}")
    mydb.commit()
    
    return True;