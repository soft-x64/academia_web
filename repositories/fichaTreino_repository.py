from database.connection import get_connection

class FichaTreinoRepository:
    
    # --- GERENCIAMENTO DA FICHA (CABEÇALHO) ---

    def inserir_ficha(self, ficha):
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            INSERT INTO ficha_treino (aluno_id, instrutor_id, data_inicio, data_vencimento, objetivo, observacoes)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (ficha.aluno_id, ficha.instrutor_id, ficha.data_inicio, ficha.data_vencimento, ficha.objetivo, ficha.observacoes)
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
            SET aluno_id = %s, instrutor_id = %s, data_inicio = %s, 
                data_vencimento = %s, objetivo = %s, observacoes = %s
            WHERE id = %s
            """,
            (ficha.aluno_id, ficha.instrutor_id, ficha.data_inicio, ficha.data_vencimento, 
             ficha.objetivo, ficha.observacoes, ficha.id)
        )
        conn.commit()
        cursor.close()
        conn.close()

    def excluir_ficha(self, ficha_id):
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            # Recomenda-se ON DELETE CASCADE na tabela item_ficha no banco de dados
            cursor.execute("DELETE FROM ficha_treino WHERE id = %s", (ficha_id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    # --- CONSULTAS (ATIVAS, VENCIDAS, TODAS) ---

    def listar_todas(self):
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            SELECT id, aluno_id, instrutor_id, data_inicio, data_vencimento, objetivo, observacoes,
                   CASE WHEN data_vencimento >= CURRENT_DATE THEN 'Ativa' ELSE 'Vencida' END as status
            FROM ficha_treino 
            ORDER BY data_vencimento DESC
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
            SELECT id, aluno_id, instrutor_id, data_inicio, data_vencimento, objetivo, observacoes, 'Ativa' as status
            FROM ficha_treino 
            WHERE data_vencimento >= CURRENT_DATE
            ORDER BY data_vencimento ASC
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
            SELECT id, aluno_id, instrutor_id, data_inicio, data_vencimento, objetivo, observacoes, 'Vencida' as status
            FROM ficha_treino 
            WHERE data_vencimento < CURRENT_DATE
            ORDER BY data_vencimento DESC
            """
        )
        resultado = cursor.fetchall()
        cursor.close()
        conn.close()
        return resultado

    # --- GERENCIAMENTO DOS ITENS DA FICHA (EXERCÍCIOS) ---

    def inserir_item_ficha(self, item):
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            INSERT INTO item_ficha (ficha_id, exercicio_id, series, repeticoes, carga, ordem, observacoes)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (item.ficha_id, item.exercicio_id, item.series, item.repeticoes, item.carga, item.ordem, item.observacoes)
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
            SELECT id, ficha_id, exercicio_id, series, repeticoes, carga, ordem, observacoes 
            FROM item_ficha 
            WHERE ficha_id = %s
            ORDER BY ordem ASC
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