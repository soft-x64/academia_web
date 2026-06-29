from database.connection import get_connection


class ConfiguracaoRepository:
    def buscar(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                id,
                nome_academia,
                cnpj,
                telefone,
                endereco,
                alertas_fichas_vencidas,
                mostrar_manutencao_dashboard,
                relatorio_semanal_email
            FROM configuracao_sistema
            WHERE id = 1
        """)

        linha = cursor.fetchone()

        cursor.close()
        conn.close()

        return linha

    def salvar(self, dados):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO configuracao_sistema (
                id,
                nome_academia,
                cnpj,
                telefone,
                endereco,
                alertas_fichas_vencidas,
                mostrar_manutencao_dashboard,
                relatorio_semanal_email,
                atualizado_em
            )
            VALUES (1, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
            ON CONFLICT (id)
            DO UPDATE SET
                nome_academia = EXCLUDED.nome_academia,
                cnpj = EXCLUDED.cnpj,
                telefone = EXCLUDED.telefone,
                endereco = EXCLUDED.endereco,
                alertas_fichas_vencidas = EXCLUDED.alertas_fichas_vencidas,
                mostrar_manutencao_dashboard = EXCLUDED.mostrar_manutencao_dashboard,
                relatorio_semanal_email = EXCLUDED.relatorio_semanal_email,
                atualizado_em = CURRENT_TIMESTAMP
        """, (
            dados["nome_academia"],
            dados["cnpj"],
            dados["telefone"],
            dados["endereco"],
            dados["alertas_fichas_vencidas"],
            dados["mostrar_manutencao_dashboard"],
            dados["relatorio_semanal_email"],
        ))

        conn.commit()
        cursor.close()
        conn.close()