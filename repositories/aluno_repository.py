from database.connection import get_connection


class AlunoRepository:

    def listar_todos(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, nome, cpf, email, telefone, peso, altura FROM aluno ORDER BY id"
        )

        resultado = cursor.fetchall()

        cursor.close()
        conn.close()

        return resultado

    def buscar_por_id(self, aluno_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, nome, cpf, email, telefone, peso, altura FROM aluno WHERE id = %s",
            (aluno_id,)
        )

        resultado = cursor.fetchone()

        cursor.close()
        conn.close()

        return resultado

    def buscar_por_cpf(self, cpf):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id FROM aluno WHERE cpf = %s",
            (cpf,)
        )

        resultado = cursor.fetchone()

        cursor.close()
        conn.close()

        return resultado

    def inserir(self, aluno):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO aluno (nome, cpf, email, telefone, peso, altura)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (
                aluno.nome,
                aluno.cpf,
                aluno.email,
                aluno.telefone,
                aluno.peso,
                aluno.altura
            )
        )

        novo_id = cursor.fetchone()[0]

        conn.commit()
        cursor.close()
        conn.close()

        return novo_id

    def atualizar(self, aluno):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE aluno
            SET nome = %s,
                cpf = %s,
                email = %s,
                telefone = %s,
                peso = %s,
                altura = %s
            WHERE id = %s
            """,
            (
                aluno.nome,
                aluno.cpf,
                aluno.email,
                aluno.telefone,
                aluno.peso,
                aluno.altura,
                aluno.id
            )
        )

        conn.commit()
        cursor.close()
        conn.close()

    def excluir(self, aluno_id):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("DELETE FROM aluno WHERE id = %s", (aluno_id,))
            conn.commit()

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cursor.close()
            conn.close()