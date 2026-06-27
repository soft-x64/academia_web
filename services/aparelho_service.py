from models.aparelho import Aparelho
from repositories.aparelho_repository import AparelhoRepository

class AparelhoService:
    def __init__(self):
        self.repository = AparelhoRepository()

    def listar(self):
        linhas = self.repository.listar_todos()
        return [
            Aparelho(id=l[0], nome=l[1], descricao=l[2], status=l[3]) 
            for l in linhas
        ]

    def buscar(self, aparelho_id):
        l = self.repository.buscar_por_id(aparelho_id)
        if not l:
            return None
        return Aparelho(id=l[0], nome=l[1], descricao=l[2], status=l[3])

    def cadastrar(self, nome, descricao, status="Disponível"):
        aparelho = Aparelho(nome=nome, descricao=descricao, status=status)
        return self.repository.inserir(aparelho)

    def editar(self, aparelho_id, nome, descricao, status):
        aparelho = Aparelho(id=aparelho_id, nome=nome, descricao=descricao, status=status)
        self.repository.atualizar(aparelho)

    def excluir(self, aparelho_id):
        self.repository.excluir(aparelho_id)