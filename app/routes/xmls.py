import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from ..service.xmls_processor import process_xml

xmls_bp = Blueprint('xmls', __name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xml'}

# Garantir que a pasta de uploads existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Verifica se a extensão do arquivo é permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@xmls_bp.route('/xml/upload', methods=['POST'])
def upload_xml():
    """Recebe um arquivo XML e processa os dados"""
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'Nenhum arquivo enviado'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'Nome de arquivo inválido'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Processar o XML
        result = process_xml(filepath)

        return jsonify({'status': 'success', 'data': result})

    return jsonify({'status': 'error', 'message': 'Extensão de arquivo não permitida'}), 400
