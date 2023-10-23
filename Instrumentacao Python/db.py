import mysql.connector
from datetime import date

mydb = mysql.connector.connect(
    host='localhost',
    port=3306,
    user='root',
    password='sptech',
    database='Streaming'
    # host='localhost',
    # port=3307,
    # user='userlimitado',
    # password='o11y',
    # database='Streaming' <-- Banco diferente
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
                "lancamento": filme[4]
            }
        )
    mydb.commit()
    return filmes

def selectOne(id):
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
        "lancamento": f[4]
    }

def insert(valores):
    cursorOps = mydb.cursor()
    cursorOps.execute(f"INSERT INTO filme (titulo, genero, direcao, lancamento) VALUES ('{valores['titulo']}', '{valores['genero']}', '{valores['direcao']}', '{date.fromisoformat(valores['lancamento']).strftime('%Y-%m-%d')}')")
    mydb.commit()

    filmes = selectAll()
    resgate = filmes[len(filmes) - 1]
    # novo = {
    #         "id": resgate[0],
    #         "titulo": resgate[1],
    #         "genero": resgate[2],
    #         "direcao": resgate[3],
    #         "lancamento": resgate[4]
    #     }

    return resgate
    # return novo

def selectByDiretor(d):
    cursorOps = mydb.cursor()
    cursorOps.execute(f"SELECT * FROM filme WHERE diretor='{d}'")
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
                "lancamento": f[4]
            }
        )
    
    return retorno

def selectByGenero(g):
    cursorOps = mydb.cursor()
    cursorOps.execute(f"SELECT * FROM filme WHERE genero LIKE %'{g}'%")
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
                "lancamento": f[4]
            }
        )
    
    return retorno