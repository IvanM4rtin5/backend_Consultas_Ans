import psycopg2.extras
from flask import Blueprint, jsonify
from ..database import get_db_connection

despesas_bp = Blueprint('despesas', __name__)

@despesas_bp.route('/despesas/trimestre', methods=['GET'])
def maiores_despesas_trimestre():
    conn = get_db_connection()
    if not conn:
        return jsonify({'status': 'error', 'message': 'Erro ao conectar ao banco'}), 500

    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = """
            WITH UltimoTrimestre AS (
                SELECT MAX(data) AS data_max FROM demonstracoes_contabeis
            )
            SELECT 
                o.razao_social, o.registro_ans, o.modalidade,
                ABS(SUM(d.vl_saldo_final)) AS total_despesas
            FROM demonstracoes_contabeis d
            JOIN operadoras_ativas o ON d.reg_ans = o.registro_ans
            JOIN UltimoTrimestre ut ON d.data = ut.data_max
            WHERE d.descricao LIKE '%ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR%'
            GROUP BY o.razao_social, o.registro_ans, o.modalidade
            ORDER BY total_despesas DESC
            LIMIT 10;
        """
        cursor.execute(query)
        resultado = cursor.fetchall()

        colunas = [desc[0] for desc in cursor.description]
        resultado_lista = [dict(zip(colunas, row)) for row in resultado]

        return jsonify({'status': 'success', 'data': resultado_lista})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

    finally:
        if conn:
            conn.close()
