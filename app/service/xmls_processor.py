import xml.etree.ElementTree as ET

def process_xml(filepath):
    """
    Processa um arquivo XML e extrai informações relevantes.
    Retorna um dicionário com os dados extraídos.
    """
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()

        # Exemplo de extração de dados do XML
        data = []
        for operadora in root.findall('Operadora'):
            registro_ans = operadora.find('RegistroANS').text if operadora.find('RegistroANS') is not None else None
            razao_social = operadora.find('RazaoSocial').text if operadora.find('RazaoSocial') is not None else None
            modalidade = operadora.find('Modalidade').text if operadora.find('Modalidade') is not None else None
            total_despesas = operadora.find('TotalDespesas').text if operadora.find('TotalDespesas') is not None else None

            data.append({
                'registro_ans': registro_ans,
                'razao_social': razao_social,
                'modalidade': modalidade,
                'total_despesas': total_despesas
            })

        return {'message': 'XML processado com sucesso', 'result': data}

    except Exception as e:
        return {'message': 'Erro ao processar XML', 'error': str(e)}

    finally:    
        tree.clear()