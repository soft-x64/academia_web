class Exercicio:
    def __init__(self, nome, grupo_muscular, descricao="", id=None):
        self.id = id
        self.nome = nome
        self.grupo_muscular = grupo_muscular
        self.descricao = descricao

    def __str__(self):
        return f"Exercício: {self.nome} ({self.grupo_muscular})"