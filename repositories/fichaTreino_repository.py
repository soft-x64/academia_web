from database.connection import get_connection


class FichaTreinoRepository:

    def inserir_ficha(self, ficha):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO ficha_treino (
                aluno_id,
                instrutor_id,
                data_inicio,
                data_vencimento,
                objetivo,
                observacoes
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (
                ficha.aluno_id,
                ficha.instrutor_id,
                ficha.data_inicio,
                ficha.data_vencimento,
                ficha.objetivo,
                ficha.observacoes,
            )
        )

        novo_id = cursor.fetchone()[0]
        conn.commit()

        cursor.close()
        conn.close()

        return novo_id

    def atualizar_ficha(self, ficha):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE ficha_treino
            SET aluno_id = %s,
                instrutor_id = %s,
                data_inicio = %s,
                data_vencimento = %s,
                objetivo = %s,
                observacoes = %s
            WHERE id = %s
            """,
            (
                ficha.aluno_id,
                ficha.instrutor_id,
                ficha.data_inicio,
                ficha.data_vencimento,
                ficha.objetivo,
                ficha.observacoes,
                ficha.id,
            )
        )

        conn.commit()
        cursor.close()
        conn.close()

    def excluir_ficha(self, ficha_id):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("DELETE FROM ficha_treino WHERE id = %s", (ficha_id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    def buscar_por_id(self, ficha_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT 
                ft.id,
                ft.aluno_id,
                ft.instrutor_id,
                ft.data_inicio,
                ft.data_vencimento,
                ft.objetivo,
                ft.observacoes,
                CASE 
                    WHEN ft.data_vencimento >= CURRENT_DATE THEN 'Ativa'
                    ELSE 'Vencida'
                END AS status,
                a.nome AS aluno_nome,
                i.nome AS instrutor_nome
            FROM ficha_treino ft
            JOIN aluno a ON a.id = ft.aluno_id
            JOIN instrutor i ON i.id = ft.instrutor_id
            WHERE ft.id = %s
            """,
            (ficha_id,)
        )

        resultado = cursor.fetchone()

        cursor.close()
        conn.close()

        return resultado

    def listar_todas(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT 
                ft.id,
                ft.aluno_id,
                ft.instrutor_id,
                ft.data_inicio,
                ft.data_vencimento,
                ft.objetivo,
                ft.observacoes,
                CASE 
                    WHEN ft.data_vencimento >= CURRENT_DATE THEN 'Ativa'
                    ELSE 'Vencida'
                END AS status,
                a.nome AS aluno_nome,
                i.nome AS instrutor_nome
            FROM ficha_treino ft
            JOIN aluno a ON a.id = ft.aluno_id
            JOIN instrutor i ON i.id = ft.instrutor_id
            ORDER BY ft.data_vencimento DESC
            """
        )

        resultado = cursor.fetchall()

        cursor.close()
        conn.close()

        return resultado

    def listar_ativas(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT 
                ft.id,
                ft.aluno_id,
                ft.instrutor_id,
                ft.data_inicio,
                ft.data_vencimento,
                ft.objetivo,
                ft.observacoes,
                'Ativa' AS status,
                a.nome AS aluno_nome,
                i.nome AS instrutor_nome
            FROM ficha_treino ft
            JOIN aluno a ON a.id = ft.aluno_id
            JOIN instrutor i ON i.id = ft.instrutor_id
            WHERE ft.data_vencimento >= CURRENT_DATE
            ORDER BY ft.data_vencimento ASC
            """
        )

        resultado = cursor.fetchall()

        cursor.close()
        conn.close()

        return resultado

    def listar_vencidas(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT 
                ft.id,
                ft.aluno_id,
                ft.instrutor_id,
                ft.data_inicio,
                ft.data_vencimento,
                ft.objetivo,
                ft.observacoes,
                'Vencida' AS status,
                a.nome AS aluno_nome,
                i.nome AS instrutor_nome
            FROM ficha_treino ft
            JOIN aluno a ON a.id = ft.aluno_id
            JOIN instrutor i ON i.id = ft.instrutor_id
            WHERE ft.data_vencimento < CURRENT_DATE
            ORDER BY ft.data_vencimento DESC
            """
        )

        resultado = cursor.fetchall()

        cursor.close()
        conn.close()

        return resultado

    def inserir_item_ficha(self, item):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO item_ficha (
                ficha_id,
                exercicio_id,
                series,
                repeticoes,
                carga,
                ordem,
                observacoes
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (
                item.ficha_id,
                item.exercicio_id,
                item.series,
                item.repeticoes,
                item.carga,
                item.ordem,
                item.observacoes,
            )
        )

        novo_id = cursor.fetchone()[0]
        conn.commit()

        cursor.close()
        conn.close()

        return novo_id

    def listar_itens_por_ficha(self, ficha_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT 
                it.id,
                it.ficha_id,
                it.exercicio_id,
                it.series,
                it.repeticoes,
                it.carga,
                it.ordem,
                it.observacoes,
                e.nome AS exercicio_nome,
                e.grupo_muscular
            FROM item_ficha it
            JOIN exercicio e ON e.id = it.exercicio_id
            WHERE it.ficha_id = %s
            ORDER BY it.ordem ASC
            """,
            (ficha_id,)
        )

        resultado = cursor.fetchall()

        cursor.close()
        conn.close()

        return resultado

    def excluir_item_ficha(self, item_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM item_ficha WHERE id = %s", (item_id,))
        conn.commit()

        cursor.close()
        conn.close()

    def listar_exercicios_mais_usados(self, limite=6):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT 
                e.id,
                e.nome,
                e.grupo_muscular,
                COUNT(it.id) AS total_usos
            FROM exercicio e
            LEFT JOIN item_ficha it ON it.exercicio_id = e.id
            GROUP BY e.id, e.nome, e.grupo_muscular
            ORDER BY total_usos DESC, e.nome ASC
            LIMIT %s
            """,
            (limite,)
        )

        resultado = cursor.fetchall()

        cursor.close()
        conn.close()

        return resultado