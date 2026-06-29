class FichaTreino:
    def __init__(self, aluno_id, instrutor_id, data_inicio, data_vencimento, objetivo, observacoes="", status="Ativa", id=None):
        self.id = id
        self.aluno_id = aluno_id
        self.instrutor_id = instrutor_id
        self.data_inicio = data_inicio
        self.data_vencimento = data_vencimento
        self.objetivo = objetivo
        self.observacoes = observacoes
        self.status = status  # Ativa ou Vencida (pode ser calculado ou armazenado)

    def __str__(self):
        return f"Ficha {self.id} - Objetivo: {self.objetivo} ({self.status})"