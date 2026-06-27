class Aparelho:
    def __init__(self, nome, descricao, status="Disponível", id=None):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.status = status

    def __str__(self):
        return f"Aparelho: {self.nome} ({self.status})"