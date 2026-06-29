from models.fichaTreino import FichaTreino
from models.itemFicha import ItemFicha
from repositories.fichaTreino_repository import FichaTreinoRepository


class FichaTreinoService:
    def __init__(self):
        self.repository = FichaTreinoRepository()

    def _montar_ficha(self, linha):
        ficha = FichaTreino(
            id=linha[0],
            aluno_id=linha[1],
            instrutor_id=linha[2],
            data_inicio=linha[3],
            data_vencimento=linha[4],
            objetivo=linha[5],
            observacoes=linha[6],
            status=linha[7],
        )

        ficha.aluno_nome = linha[8]
        ficha.instrutor_nome = linha[9]

        return ficha

    def criar_ficha(self, aluno_id, instrutor_id, data_inicio, data_vencimento, objetivo, observacoes=""):
        ficha = FichaTreino(
            aluno_id=aluno_id,
            instrutor_id=instrutor_id,
            data_inicio=data_inicio,
            data_vencimento=data_vencimento,
            objetivo=objetivo,
            observacoes=observacoes,
        )

        return self.repository.inserir_ficha(ficha)

    def editar_ficha(self, ficha_id, aluno_id, instrutor_id, data_inicio, data_vencimento, objetivo, observacoes=""):
        ficha = FichaTreino(
            id=ficha_id,
            aluno_id=aluno_id,
            instrutor_id=instrutor_id,
            data_inicio=data_inicio,
            data_vencimento=data_vencimento,
            objetivo=objetivo,
            observacoes=observacoes,
        )

        self.repository.atualizar_ficha(ficha)

    def excluir_ficha(self, ficha_id):
        self.repository.excluir_ficha(ficha_id)

    def buscar_ficha(self, ficha_id):
        linha = self.repository.buscar_por_id(ficha_id)

        if not linha:
            return None

        return self._montar_ficha(linha)

    def listar_fichas(self, filtro_status="Todas"):
        if filtro_status == "Ativas":
            linhas = self.repository.listar_ativas()
        elif filtro_status == "Vencidas":
            linhas = self.repository.listar_vencidas()
        else:
            linhas = self.repository.listar_todas()

        return [self._montar_ficha(linha) for linha in linhas]

    def adicionar_exercicio_na_ficha(self, ficha_id, exercicio_id, series, repeticoes, carga, ordem, observacoes=""):
        item = ItemFicha(
            ficha_id=ficha_id,
            exercicio_id=exercicio_id,
            series=series,
            repeticoes=repeticoes,
            carga=carga,
            ordem=ordem,
            observacoes=observacoes,
        )

        return self.repository.inserir_item_ficha(item)

    def obter_exercicios_da_ficha(self, ficha_id):
        linhas = self.repository.listar_itens_por_ficha(ficha_id)

        itens = []

        for linha in linhas:
            item = ItemFicha(
                id=linha[0],
                ficha_id=linha[1],
                exercicio_id=linha[2],
                series=linha[3],
                repeticoes=linha[4],
                carga=linha[5],
                ordem=linha[6],
                observacoes=linha[7],
            )

            item.exercicio_nome = linha[8]
            item.grupo_muscular = linha[9]

            itens.append(item)

        return itens

    def remover_exercicio_da_ficha(self, item_id):
        self.repository.excluir_item_ficha(item_id)

    def listar_exercicios_mais_usados(self, limite=6):
        linhas = self.repository.listar_exercicios_mais_usados(limite)

        return [
            {
                "id": linha[0],
                "nome": linha[1],
                "grupo_muscular": linha[2],
                "total_usos": linha[3],
            }
            for linha in linhas
        ]