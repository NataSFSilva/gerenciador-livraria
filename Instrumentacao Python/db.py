import mysql.connector
from datetime import date

mydb = mysql.connector.connect(
    host='localhost',
    user='userlimitado',
    password='o11y',
    database='Streaming'
)

cursorOps = mydb.cursor()

def selectAll():
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
    cursorOps.execute(f"SELECT * FROM filme WHERE id = {id}")
    filme = cursorOps.fetchall()

    if len(filme) == 0:
        return None
    
    return {
        "id": filme[0],
        "titulo": filme[1],
        "direcao": filme[2],
        "genero": filme[3],
        "lancamento": filme[4]
    }

def insert(valores):
    cursorOps.execute(f"INSERT INTO filme (titulo, genero, direcao, lancamento) VALUES ('{valores['titulo']}', '{valores['genero']}', '{valores['direcao']}', '{date.fromisoformat(valores['lancamento']).strftime('%Y-%m-%d')}'")

    retorno = cursorOps.fetchall()

    print(retorno)

    # filmes = selectAll()
    # resgate = filmes[len(filmes) - 1]
    # novo = {
    #         "id": resgate[0],
    #         "titulo": resgate[1],
    #         "genero": resgate[2],
    #         "direcao": resgate[3],
    #         "lancamento": resgate[4]
    #     }

    # return novo
