import model
import json
from datetime import date

Filmes = [
    {
        'id': 1,
        'titulo': "Um Corpo que cai",
        'genero': "Suspense",
        'direcao': "Hitchcock",
        'lancamento': "1958-07-21"
    },
    {
        'id': 2,
        'titulo': "Psicose",
        'genero': "Suspense, terror",
        'direcao': "Hitchcock",
        'lancamento': "1961-11-01"
    },
    {
        'id': 3,
        'titulo': "Tempos Modernos",
        'genero': "Comédia, romance",
        'direcao': "Charlie Chaplin",
        'lancamento': "1936-02-25"
    }
]


def insert(valores):
    id: int

    if len(Filmes) == 0:
        id = 1
    else:
        id = Filmes[- 1]['id'] + 1

    novo = model.Filme(id, valores['titulo'], valores['genero'],
                       valores['direcao'], date.fromisoformat(valores['lancamento']).strftime("%Y-%m-%d"))

    Filmes.append(json.dumps(novo.__dict__))

    return novo
