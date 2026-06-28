from models.aluno import Aluno
from repositories.aluno_repository import AlunoRepository

class CPFDuplicadoError(Exception):
    pass

class AlunoService:
    def __init__(self):
        self.repository = AlunoRepository()

    def listar(self):
        linhas = self.repository.listar_todos()
        return [Aluno(id=l[0], nome=l[1], cpf=l[2], email=l[3], telefone=l[4], peso=l[5], altura=l[6]) for l in linhas]

    def buscar(self, aluno_id):
        l = self.repository.buscar_por_id(aluno_id)
        if not l:
            return None
        return Aluno(id=l[0], nome=l[1], cpf=l[2], email=l[3], telefone=l[4], peso=l[5], altura=l[6])

    def cadastrar(self, nome, cpf, email, telefone, peso, altura):
        if self.repository.buscar_por_cpf(cpf):
            raise CPFDuplicadoError(f"Já existe um aluno com o CPF {cpf}")
        aluno = Aluno(nome=nome, cpf=cpf, email=email, telefone=telefone, peso=peso, altura=altura)
        return self.repository.inserir(aluno)

    def editar(self, aluno_id, nome, cpf, email, telefone, peso, altura):
        aluno_existente = self.repository.buscar_por_cpf(cpf)

        if aluno_existente and aluno_existente[0] != aluno_id:
            raise CPFDuplicadoError(f"Já existe outro aluno cadastrado com o CPF {cpf}")

        aluno = Aluno(
            id=aluno_id,
            nome=nome,
            cpf=cpf,
            email=email,
            telefone=telefone,
            peso=peso,
            altura=altura
        )

        self.repository.atualizar(aluno)

    def excluir(self, aluno_id):
        self.repository.excluir(aluno_id)