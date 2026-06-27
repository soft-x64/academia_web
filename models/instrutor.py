# models/instrutor.py
class Instrutor:
    def __init__(self, nome, cpf, email, telefone, cref, especialidade, id=None):
        self.id = id
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.telefone = telefone
        self.cref = cref
        self.especialidade = especialidade

    def __str__(self):
        return f"{self.nome} (CREF: {self.cref})"