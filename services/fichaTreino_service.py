from models.fichaTreino import FichaTreino
from models.itemFicha import ItemFicha
from repositories.fichaTreino_repository import FichaTreinoRepository

class FichaTreinoService:
    def __init__(self):
        self.repository = FichaTreinoRepository()

    # --- REGRAS DE NEGÓCIO: FICHA ---

    def criar_ficha(self, aluno_id, instrutor_id, data_inicio, data_vencimento, objetivo, observacoes=""):
        ficha = FichaTreino(
            aluno_id=aluno_id, 
            instrutor_id=instrutor_id, 
            data_inicio=data_inicio, 
            data_vencimento=data_vencimento, 
            objetivo=objetivo, 
            observacoes=observacoes
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
            observacoes=observacoes
        )
        self.repository.atualizar_ficha(ficha)

    def excluir_ficha(self, ficha_id):
        self.repository.excluir_ficha(ficha_id)

    # --- REGRAS DE NEGÓCIO: CONSULTAS ---

    def listar_fichas(self, filtro_status="Todas"):
        """Retorna as fichas baseadas no filtro (Todas, Ativas ou Vencidas)"""
        if filtro_status == "Ativas":
            linhas = self.repository.listar_ativas()
        elif filtro_status == "Vencidas":
            linhas = self.repository.listar_vencidas()
        else:
            linhas = self.repository.listar_todas()

        return [
            FichaTreino(id=l[0], aluno_id=l[1], instrutor_id=l[2], data_inicio=l[3], 
                        data_vencimento=l[4], objetivo=l[5], observacoes=l[6], status=l[7]) 
            for l in linhas
        ]

    # --- REGRAS DE NEGÓCIO: ITENS DA FICHA ---

    def adicionar_exercicio_na_ficha(self, ficha_id, exercicio_id, series, repeticoes, carga, ordem, observacoes=""):
        item = ItemFicha(
            ficha_id=ficha_id,
            exercicio_id=exercicio_id,
            series=series,
            repeticoes=repeticoes,
            carga=carga,
            ordem=ordem,
            observacoes=observacoes
        )
        return self.repository.inserir_item_ficha(item)

    def obter_exercicios_da_ficha(self, ficha_id):
        linhas = self.repository.listar_itens_por_ficha(ficha_id)
        return [
            ItemFicha(id=l[0], ficha_id=l[1], exercicio_id=l[2], series=l[3], 
                      repeticoes=l[4], carga=l[5], ordem=l[6], observacoes=l[7]) 
            for l in linhas
        ]

    def remover_exercicio_da_ficha(self, item_id):
        self.repository.excluir_item_ficha(item_id)