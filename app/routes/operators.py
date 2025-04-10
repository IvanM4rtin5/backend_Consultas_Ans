from flask import jsonify
from ..database import get_db
from sqlalchemy import text
from flask import Blueprint

operators_bp = Blueprint('operators', __name__)

@operators_bp.route('/operators', methods=['GET'])
def get_operators():
    session = (get_db())
    if not session:
        return jsonify({'status': 'error', 'message': 'Banco de dados fora do ar'}), 500

    try:
        query = text("SELECT * FROM operadoras_ativas")
        resultado = session.execute(query)
        colunas = resultado.keys()
        resultado_lista = [dict(zip(colunas, row)) for row in resultado]

        return jsonify({'status': 'success', 'data': resultado_lista})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500 

    finally:
        session.close()