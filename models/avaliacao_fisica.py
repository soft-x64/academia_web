from datetime import date

class AvaliacaoFisica:
    def __init__(self, aluno_id, data_avaliacao, peso, percentual_gordura=None, observacoes="", id=None):
        self.id = id
        self.aluno_id = aluno_id
        self.data_avaliacao = data_avaliacao or date.today()
        self.peso = peso
        self.percentual_gordura = percentual_gordura
        self.observacoes = observacoes

    def __str__(self):
        return f"Avaliação de {self.data_avaliacao}: {self.peso}kg, {self.percentual_gordura}% gordura"