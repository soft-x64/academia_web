from models.instrutor import Instrutor
from repositories.instrutor_repository import InstrutorRepository
from services.aluno_service import CPFDuplicadoError 

class CREFDuplicadoError(Exception):
    pass

class InstrutorService:
    def __init__(self):
        self.repository = InstrutorRepository()

    def listar(self):
        linhas = self.repository.listar_todos()
        return [
            Instrutor(id=l[0], nome=l[1], cpf=l[2], email=l[3], telefone=l[4], cref=l[5], especialidade=l[6])
            for l in linhas
        ]

    def buscar(self, instrutor_id):
        l = self.repository.buscar_por_id(instrutor_id)
        if not l:
            return None
        return Instrutor(id=l[0], nome=l[1], cpf=l[2], email=l[3], telefone=l[4], cref=l[5], especialidade=l[6])

    def cadastrar(self, nome, cpf, email, telefone, cref, especialidade):
        if self.repository.buscar_por_cpf(cpf):
             raise CPFDuplicadoError(f"Já existe um instrutor com o CPF {cpf}")

        if self.repository.buscar_por_cref(cref):
             raise CREFDuplicadoError(f"Já existe um instrutor com o CREF {cref}")

        instrutor = Instrutor(
            nome=nome,
            cpf=cpf,
            email=email,
            telefone=telefone,
            cref=cref,
            especialidade=especialidade
    )

        return self.repository.inserir(instrutor)
  
    def editar(self, instrutor_id, nome, cpf, email, telefone, cref, especialidade):
        instrutor = Instrutor(id=instrutor_id, nome=nome, cpf=cpf, email=email, telefone=telefone,
                               cref=cref, especialidade=especialidade)
        self.repository.atualizar(instrutor)

    def excluir(self, instrutor_id):
        self.repository.excluir(instrutor_id)