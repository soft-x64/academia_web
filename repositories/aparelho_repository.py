from database.connection import get_connection

class AparelhoRepository:
    def listar_todos(self):
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT id, nome, descricao, status FROM aparelho ORDER BY nome"
        )
        resultado = cursor.fetchall()
        
        cursor.close()
        conn.close()
        return resultado

    def buscar_por_id(self, aparelho_id):
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT id, nome, descricao, status FROM aparelho WHERE id = %s",
            (aparelho_id,)
        )
        resultado = cursor.fetchone()
        
        cursor.close()
        conn.close()
        return resultado

    def inserir(self, aparelho):
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            INSERT INTO aparelho (nome, descricao, status)
            VALUES (%s, %s, %s)
            RETURNING id
            """,
            (aparelho.nome, aparelho.descricao, aparelho.status)
        )
        
        novo_id = cursor.fetchone()[0]
        conn.commit()
        
        cursor.close()
        conn.close()
        return novo_id

    def atualizar(self, aparelho):
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            UPDATE aparelho
            SET nome = %s,
                descricao = %s,
                status = %s
            WHERE id = %s
            """,
            (aparelho.nome, aparelho.descricao, aparelho.status, aparelho.id)
        )
        
        conn.commit()
        cursor.close()
        conn.close()

    def excluir(self, aparelho_id):
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM aparelho WHERE id = %s", (aparelho_id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()