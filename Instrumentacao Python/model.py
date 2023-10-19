from datetime import date


class Filme():
    def __init__(self, id: int, titulo: str, genero: str, direcao: str, lancamento: date):
        self._id = id
        self._titulo = titulo
        self._genero = genero
        self._direcao = direcao
        self._lancamento = lancamento

    @property
    def id(self):
        return self._id

    @property
    def titulo(self):
        return self._titulo

    @titulo.setter
    def titulo(self, titulo):
        self._titulo = titulo

    @property
    def genero(self):
        return self._genero

    @genero.setter
    def genero(self, genero):
        self._genero = genero

    @property
    def direcao(self):
        return self._direcao

    @direcao.setter
    def direcao(self, direcao):
        self._direcao = direcao

    @property
    def lancamento(self):
        return self._lancamento

    @lancamento.setter
    def lancamento(self, lancamento):
        self._lancamento = lancamento

    def __str__(self):
        return f"Filme(id={self.id},
            titulo='{self.titulo}',
            genero='{self.genero}',
            direcao='{self.direcao}',
            lancamento='{self.lancamento}')"