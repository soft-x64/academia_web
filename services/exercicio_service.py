from models.exercicio import Exercicio
from models.aparelho import Aparelho
from repositories.exercicio_repository import ExercicioRepository

class ExercicioService:
    def __init__(self):
        self.repository = ExercicioRepository()

    def listar(self):
        linhas = self.repository.listar_todos()
        return [
            Exercicio(id=l[0], nome=l[1], grupo_muscular=l[2], descricao=l[3]) 
            for l in linhas
        ]

    def buscar(self, exercicio_id):
        l = self.repository.buscar_por_id(exercicio_id)
        if not l:
            return None
        return Exercicio(id=l[0], nome=l[1], grupo_muscular=l[2], descricao=l[3])

    def cadastrar(self, nome, grupo_muscular, descricao=""):
        exercicio = Exercicio(nome=nome, grupo_muscular=grupo_muscular, descricao=descricao)
        return self.repository.inserir(exercicio)

    def editar(self, exercicio_id, nome, grupo_muscular, descricao):
        exercicio = Exercicio(id=exercicio_id, nome=nome, grupo_muscular=grupo_muscular, descricao=descricao)
        self.repository.atualizar(exercicio)

    def excluir(self, exercicio_id):
        self.repository.excluir(exercicio_id)

    # --- GERENCIAMENTO DE APARELHOS VINCULADOS ---

    def adicionar_aparelho(self, exercicio_id, aparelho_id):
        # Aqui pode entrar uma validação extra se o aparelho existe antes de vincular
        self.repository.vincular_aparelho(exercicio_id, aparelho_id)

    def obter_aparelhos(self, exercicio_id):
        linhas = self.repository.listar_aparelhos_vinculados(exercicio_id)
        return [
            Aparelho(id=l[0], nome=l[1], descricao=l[2], status=l[3]) 
            for l in linhas
        ]