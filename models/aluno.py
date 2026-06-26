class Aluno:
    def __init__(self, nome, cpf, email, telefone, peso, altura, id=None):
        self.id = id
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.telefone = telefone
        self.peso = peso
        self.altura = altura

    def __str__(self):
        return f"{self.nome} (CPF: {self.cpf})"