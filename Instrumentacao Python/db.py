import mysql.connector
from datetime import date

mydb = mysql.connector.connect(
    host='localhost',
    port=3306,
    user='root',
    password='prvzcpy',
    database='Streaming'
)

def selectAll():
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
    mydb.commit()
    return filmes

def selectById(id):
    cursorOps = mydb.cursor()
    cursorOps.execute(f"SELECT * FROM filme WHERE id = {id}")
    filme = cursorOps.fetchall()

    if len(filme) == 0:
        return None
    
    f = filme[0]
    return {
        "id": f[0],
        "titulo": f[1],
        "direcao": f[2],
        "genero": f[3],
        "lancamento": f[4].strftime("%Y-%m-%d")
    }

def insert(valores):
    cursorOps = mydb.cursor()
    cursorOps.execute(f"INSERT INTO filme (titulo, genero, direcao, lancamento) VALUES ('{valores['titulo']}', '{valores['genero']}', '{valores['direcao']}', '{date.fromisoformat(valores['lancamento']).strftime('%Y-%m-%d')}')")
    mydb.commit()

    filmes = selectAll()
    novo = filmes[len(filmes) - 1]

    return novo

def selectByDiretor(d):
    cursorOps = mydb.cursor()
    cursorOps.execute(f"SELECT * FROM filme WHERE direcao='{d}'")
    filmes = cursorOps.fetchall()

    if len(filmes) == 0:
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
    cursorOps = mydb.cursor()
    cursorOps.execute(f"SELECT * FROM filme WHERE genero LIKE '%{g}%'")
    filmes = cursorOps.fetchall()

    if len(filmes) == 0:
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
    if (body['titulo'] == None or body['direcao'] == None or body['genero'] == None or body['lancamento'] == None) or selectById(id) == None:
        return False
    
    comando = f"UPDATE filme SET titulo = '{body['titulo']}', direcao = '{body['direcao']}', genero = '{body['genero']}', lancamento = '{body['lancamento']}' WHERE id = {id}"
    cursorOps = mydb.cursor()
    cursorOps.execute(comando)
    mydb.commit()

    return True;

def delete(id: int):
    if selectById(id) == None:
        return False

    cursorOps = mydb.cursor()
    cursorOps.execute(f"DELETE FROM filme WHERE id={id}")
    mydb.commit()
    
    return True;