from datetime import date

class Filme():
    def __init__(self, id: int, titulo: str, genero: str, direcao: str, lancamento: date):
        self.id = id
        self.titulo = titulo
        self.genero = genero
        self.direcao = direcao
        self.lancamento = lancamento

@property.getter
def getId(self):
    return self.id

@property.getter
def getTitulo(self):
    return self.titulo

@titulo.setter
def setTitulo(self, titulo: str):
    self.titulo = titulo

@property
def getGenero(self):
    return self.genero

@genero.setter
def setGenero(self, genero: str):
    self.genero = genero

@property
def getDirecao(self):
    return self.direcao

@direcao.setter
def setDirecao(self, direcao: str):
    self.direcao = direcao

@property
def getLancamento(self):
    return self.lancamento

@lancamento.setter
def setLancamento(self, lancamento):
    self.lancamento = lancamento