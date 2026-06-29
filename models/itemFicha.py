class ItemFicha:
    def __init__(self, ficha_id, exercicio_id, series, repeticoes, carga, ordem, observacoes="", id=None):
        self.id = id
        self.ficha_id = ficha_id
        self.exercicio_id = exercicio_id
        self.series = series
        self.repeticoes = repeticoes
        self.carga = carga
        self.ordem = ordem
        self.observacoes = observacoes

    def __str__(self):
        return f"Item {self.ordem}: Exercício ID {self.exercicio_id} ({self.series}x{self.repeticoes})"