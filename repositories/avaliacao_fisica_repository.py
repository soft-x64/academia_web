from database.connection import get_connection

class AvaliacaoFisicaRepository:

    def listar_por_aluno(self, aluno_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT id, aluno_id, data_avaliacao, peso, percentual_gordura, observacoes
               FROM avaliacao_fisica WHERE aluno_id = %s ORDER BY data_avaliacao DESC""",
            (aluno_id,)
        )
        resultado = cursor.fetchall()
        cursor.close()
        conn.close()
        return resultado

    def buscar_por_id(self, avaliacao_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT id, aluno_id, data_avaliacao, peso, percentual_gordura, observacoes
               FROM avaliacao_fisica WHERE id = %s""",
            (avaliacao_id,)
        )
        resultado = cursor.fetchone()
        cursor.close()
        conn.close()
        return resultado

    def inserir(self, avaliacao):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO avaliacao_fisica (aluno_id, data_avaliacao, peso, percentual_gordura, observacoes)
               VALUES (%s, %s, %s, %s, %s) RETURNING id""",
            (avaliacao.aluno_id, avaliacao.data_avaliacao, avaliacao.peso,
             avaliacao.percentual_gordura, avaliacao.observacoes)
        )
        novo_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return novo_id

    def atualizar(self, avaliacao):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """UPDATE avaliacao_fisica SET data_avaliacao=%s, peso=%s, percentual_gordura=%s, observacoes=%s
               WHERE id=%s""",
            (avaliacao.data_avaliacao, avaliacao.peso, avaliacao.percentual_gordura,
             avaliacao.observacoes, avaliacao.id)
        )
        conn.commit()
        cursor.close()
        conn.close()

    def excluir(self, avaliacao_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM avaliacao_fisica WHERE id = %s", (avaliacao_id,))
        conn.commit()
        cursor.close()
        conn.close()
        
    def listar_ultimas(self, limite=4):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                af.id,
                a.nome AS aluno_nome,
                af.data_avaliacao,
                af.peso,
                af.percentual_gordura
            FROM avaliacao_fisica af
            JOIN aluno a ON a.id = af.aluno_id
            ORDER BY af.data_avaliacao DESC, af.id DESC
            LIMIT %s
        """, (limite,))

        resultados = cursor.fetchall()

        cursor.close()
        conn.close()

        return [
            {
                "id": linha[0],
                "aluno_nome": linha[1],
                "data_avaliacao": linha[2],
                "peso": linha[3],
                "percentual_gordura": linha[4]
            }
            for linha in resultados
        ]


    def contar_avaliacoes_no_mes(self, ano, mes):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM avaliacao_fisica
            WHERE EXTRACT(YEAR FROM data_avaliacao) = %s
            AND EXTRACT(MONTH FROM data_avaliacao) = %s
        """, (ano, mes))

        total = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return total    