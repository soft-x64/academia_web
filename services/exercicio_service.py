from models.exercicio import Exercicio
from models.aparelho import Aparelho
from repositories.exercicio_repository import ExercicioRepository


class ExercicioService:
    def __init__(self):
        self.repository = ExercicioRepository()

    def listar(self):
        linhas = self.repository.listar_todos()

        exercicios = []

        for linha in linhas:
            exercicio = Exercicio(
                id=linha[0],
                nome=linha[1],
                grupo_muscular=linha[2],
                descricao=linha[3],
            )

            exercicio.aparelhos = linha[4] if len(linha) > 4 else ""

            exercicios.append(exercicio)

        return exercicios

    def buscar(self, exercicio_id):
        linha = self.repository.buscar_por_id(exercicio_id)

        if not linha:
            return None

        return Exercicio(
            id=linha[0],
            nome=linha[1],
            grupo_muscular=linha[2],
            descricao=linha[3],
        )

    def cadastrar(self, nome, grupo_muscular, descricao=""):
        exercicio = Exercicio(
            nome=nome,
            grupo_muscular=grupo_muscular,
            descricao=descricao,
        )

        return self.repository.inserir(exercicio)

    def editar(self, exercicio_id, nome, grupo_muscular, descricao):
        exercicio = Exercicio(
            id=exercicio_id,
            nome=nome,
            grupo_muscular=grupo_muscular,
            descricao=descricao,
        )

        self.repository.atualizar(exercicio)

    def excluir(self, exercicio_id):
        self.repository.excluir(exercicio_id)

    def adicionar_aparelho(self, exercicio_id, aparelho_id):
        self.repository.vincular_aparelho(exercicio_id, aparelho_id)

    def atualizar_aparelhos(self, exercicio_id, aparelhos_ids):
        self.repository.remover_aparelhos_vinculados(exercicio_id)

        for aparelho_id in aparelhos_ids:
            if aparelho_id:
                self.repository.vincular_aparelho(exercicio_id, int(aparelho_id))

    def obter_aparelhos(self, exercicio_id):
        linhas = self.repository.listar_aparelhos_vinculados(exercicio_id)

        return [
            Aparelho(id=l[0], nome=l[1], descricao=l[2], status=l[3])
            for l in linhas
        ]

    def obter_ids_aparelhos(self, exercicio_id):
        aparelhos = self.obter_aparelhos(exercicio_id)
        return [aparelho.id for aparelho in aparelhos]