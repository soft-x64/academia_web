from database.connection import get_connection

class InstrutorRepository:

    def listar_todos(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, cpf, email, telefone, cref, especialidade FROM instrutor ORDER BY id")
        resultado = cursor.fetchall()
        cursor.close()
        conn.close()
        return resultado

    def buscar_por_id(self, instrutor_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, nome, cpf, email, telefone, cref, especialidade FROM instrutor WHERE id = %s",
            (instrutor_id,)
        )
        resultado = cursor.fetchone()
        cursor.close()
        conn.close()
        return resultado

    def buscar_por_cpf(self, cpf):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM instrutor WHERE cpf = %s", (cpf,))
        resultado = cursor.fetchone()
        cursor.close()
        conn.close()
        return resultado
    
    def buscar_por_cref(self, cref):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM instrutor WHERE cref = %s", (cref,))
        resultado = cursor.fetchone()
        cursor.close()
        conn.close()
        return resultado

    def inserir(self, instrutor):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO instrutor (nome, cpf, email, telefone, cref, especialidade)
               VALUES (%s, %s, %s, %s, %s, %s) RETURNING id""",
            (instrutor.nome, instrutor.cpf, instrutor.email, instrutor.telefone,
             instrutor.cref, instrutor.especialidade)
        )
        novo_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return novo_id

    def atualizar(self, instrutor):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """UPDATE instrutor SET nome=%s, cpf=%s, email=%s, telefone=%s, cref=%s, especialidade=%s
               WHERE id=%s""",
            (instrutor.nome, instrutor.cpf, instrutor.email, instrutor.telefone,
             instrutor.cref, instrutor.especialidade, instrutor.id)
        )
        conn.commit()
        cursor.close()
        conn.close()

    def excluir(self, instrutor_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM instrutor WHERE id = %s", (instrutor_id,))
        conn.commit()
        cursor.close()
        conn.close()