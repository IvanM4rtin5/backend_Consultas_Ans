from flask import Blueprint, jsonify
from sqlalchemy import text
from ..database import get_db

despesas_bp = Blueprint('despesas', __name__)

@despesas_bp.route('/despesas/trimestre', methods=['GET'])
def maiores_despesas_trimestre():
    session = (get_db())

    try:
        query = text("""
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
        """)

        resultado = session.execute(query)
        colunas = resultado.keys()
        resultado_lista = [dict(zip(colunas, row)) for row in resultado]

        return jsonify({'status': 'success', 'data': resultado_lista})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

    finally:
        session.close()
