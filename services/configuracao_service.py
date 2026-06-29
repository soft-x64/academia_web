from repositories.configuracao_repository import ConfiguracaoRepository


class ConfiguracaoService:
    def __init__(self):
        self.repository = ConfiguracaoRepository()

    def buscar(self):
        linha = self.repository.buscar()

        if not linha:
            return {
                "nome_academia": "TrainerX64",
                "cnpj": "",
                "telefone": "",
                "endereco": "",
                "alertas_fichas_vencidas": True,
                "mostrar_manutencao_dashboard": True,
                "relatorio_semanal_email": False,
            }

        return {
            "id": linha[0],
            "nome_academia": linha[1],
            "cnpj": linha[2],
            "telefone": linha[3],
            "endereco": linha[4],
            "alertas_fichas_vencidas": linha[5],
            "mostrar_manutencao_dashboard": linha[6],
            "relatorio_semanal_email": linha[7],
        }

    def salvar(self, nome_academia, cnpj, telefone, endereco,
               alertas_fichas_vencidas,
               mostrar_manutencao_dashboard,
               relatorio_semanal_email):

        dados = {
            "nome_academia": nome_academia.strip() or "TrainerX64",
            "cnpj": cnpj.strip(),
            "telefone": telefone.strip(),
            "endereco": endereco.strip(),
            "alertas_fichas_vencidas": alertas_fichas_vencidas,
            "mostrar_manutencao_dashboard": mostrar_manutencao_dashboard,
            "relatorio_semanal_email": relatorio_semanal_email,
        }

        self.repository.salvar(dados)