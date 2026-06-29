from database.connection import get_connection


class ExercicioRepository:
    def listar_todos(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT 
                e.id,
                e.nome,
                e.grupo_muscular,
                e.descricao,
                COALESCE(STRING_AGG(a.nome, ', ' ORDER BY a.nome), '') AS aparelhos
            FROM exercicio e
            LEFT JOIN exercicio_aparelho ea ON ea.exercicio_id = e.id
            LEFT JOIN aparelho a ON a.id = ea.aparelho_id
            GROUP BY e.id, e.nome, e.grupo_muscular, e.descricao
            ORDER BY e.nome
            """
        )

        resultado = cursor.fetchall()

        cursor.close()
        conn.close()

        return resultado

    def buscar_por_id(self, exercicio_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, nome, grupo_muscular, descricao FROM exercicio WHERE id = %s",
            (exercicio_id,)
        )

        resultado = cursor.fetchone()

        cursor.close()
        conn.close()

        return resultado

    def inserir(self, exercicio):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO exercicio (nome, grupo_muscular, descricao)
            VALUES (%s, %s, %s)
            RETURNING id
            """,
            (exercicio.nome, exercicio.grupo_muscular, exercicio.descricao)
        )

        novo_id = cursor.fetchone()[0]
        conn.commit()

        cursor.close()
        conn.close()

        return novo_id

    def atualizar(self, exercicio):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE exercicio
            SET nome = %s,
                grupo_muscular = %s,
                descricao = %s
            WHERE id = %s
            """,
            (
                exercicio.nome,
                exercicio.grupo_muscular,
                exercicio.descricao,
                exercicio.id,
            )
        )

        conn.commit()
        cursor.close()
        conn.close()

    def excluir(self, exercicio_id):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("DELETE FROM exercicio WHERE id = %s", (exercicio_id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    def vincular_aparelho(self, exercicio_id, aparelho_id):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO exercicio_aparelho (exercicio_id, aparelho_id)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING
                """,
                (exercicio_id, aparelho_id)
            )

            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    def remover_aparelhos_vinculados(self, exercicio_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM exercicio_aparelho WHERE exercicio_id = %s",
            (exercicio_id,)
        )

        conn.commit()

        cursor.close()
        conn.close()

    def listar_aparelhos_vinculados(self, exercicio_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT 
                a.id,
                a.nome,
                a.descricao,
                a.status
            FROM aparelho a
            INNER JOIN exercicio_aparelho ea ON a.id = ea.aparelho_id
            WHERE ea.exercicio_id = %s
            ORDER BY a.nome
            """,
            (exercicio_id,)
        )

        resultado = cursor.fetchall()

        cursor.close()
        conn.close()

        return resultado