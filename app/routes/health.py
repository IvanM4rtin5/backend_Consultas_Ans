from flask import Blueprint, jsonify, request
from sqlalchemy import text
from ..database import get_db
import traceback

search_bp = Blueprint('search', __name__)

@search_bp.route('/seach_operators', methods=['POST'])
def search_operators():
    conn = get_db()
    if not conn:
        return jsonify({'status': 'error', 'message': 'Banco de dados fora do ar'}), 500
    
    data = request.get_json()
    razao_social = data.get('razao_social')

    if not razao_social:
        return jsonify({'status': 'error', 'message': 'razao_social is required'}), 400

    try:
        query = text("SELECT * FROM operadoras_ativas WHERE razao_social ILIKE :razao_social")

        paramentro = f"%{razao_social}%"    
        resultado = conn.execute(query, {'razao_social': paramentro})
        colunas = resultado.keys()
        resultado_lista = [dict(zip(colunas, row)) for row in resultado]

        if not resultado_lista:
            return jsonify({'status': 'error', 'message': 'Operadora nao encontrada'}), 404

        return jsonify({'status': 'success', 'data': resultado_lista})   

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'status': 'error', 'message': str(e)}), 500

    finally:
        if conn:
            conn.close()
