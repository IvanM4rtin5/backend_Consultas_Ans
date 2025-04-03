from flask import Blueprint, jsonify
from ..database import get_db_connection

health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    conn = get_db_connection()
    if not conn:
        return jsonify({'status': 'error', 'message': 'Banco de dados fora do ar'}), 500

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM operadoras_ativas")
        count = cursor.fetchone()[0]

        return jsonify({'status': 'up', 'total_operadoras': count})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

    finally:
        if conn:
            conn.close()
