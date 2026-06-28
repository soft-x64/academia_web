from models.avaliacao_fisica import AvaliacaoFisica
from repositories.avaliacao_fisica_repository import AvaliacaoFisicaRepository

class ValorInvalidoError(Exception):
    pass

class AvaliacaoFisicaService:
    def __init__(self):
        self.repository = AvaliacaoFisicaRepository()

    def listar_por_aluno(self, aluno_id):
        linhas = self.repository.listar_por_aluno(aluno_id)
        return [
            AvaliacaoFisica(id=l[0], aluno_id=l[1], data_avaliacao=l[2], peso=l[3],
                             percentual_gordura=l[4], observacoes=l[5])
            for l in linhas
        ]

    def buscar(self, avaliacao_id):
        l = self.repository.buscar_por_id(avaliacao_id)
        if not l:
            return None
        return AvaliacaoFisica(id=l[0], aluno_id=l[1], data_avaliacao=l[2], peso=l[3],
                                percentual_gordura=l[4], observacoes=l[5])

    def cadastrar(self, aluno_id, data_avaliacao, peso, percentual_gordura, observacoes):
        if percentual_gordura is not None and not (0 <= percentual_gordura <= 100):
            raise ValorInvalidoError("Percentual de gordura deve estar entre 0 e 100")
        avaliacao = AvaliacaoFisica(
            aluno_id=aluno_id, data_avaliacao=data_avaliacao, peso=peso,
            percentual_gordura=percentual_gordura, observacoes=observacoes
        )
        return self.repository.inserir(avaliacao)

    def editar(self, avaliacao_id, aluno_id, data_avaliacao, peso, percentual_gordura, observacoes):
        if percentual_gordura is not None and not (0 <= percentual_gordura <= 100):
            raise ValorInvalidoError("Percentual de gordura deve estar entre 0 e 100")
        avaliacao = AvaliacaoFisica(
            id=avaliacao_id, aluno_id=aluno_id, data_avaliacao=data_avaliacao,
            peso=peso, percentual_gordura=percentual_gordura, observacoes=observacoes
        )
        self.repository.atualizar(avaliacao)

    def excluir(self, avaliacao_id):
        self.repository.excluir(avaliacao_id)
    
    def listar_ultimas(self, limite=4):
        return self.repository.listar_ultimas(limite)


    def contar_avaliacoes_no_mes(self, ano, mes):
        return self.repository.contar_avaliacoes_no_mes(ano, mes)