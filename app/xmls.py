import os
import pandas as pd
import xml.etree.ElementTree as ET
import glob
import re
from datetime import datetime
import psycopg2
from psycopg2.extras import execute_values

def process_xml_file(file_path):
    """Processa um arquivo XML de demonstrações contábeis da ANS"""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        records = []
        
        # Extrair a data do nome do arquivo (normalmente segue padrão como 1T2023, 2T2023, etc.)
        file_name = os.path.basename(file_path)
        date_match = re.search(r'(\d)T(\d{4})', file_name)
        
        if date_match:
            trimester = int(date_match.group(1))
            year = int(date_match.group(2))
            # Definir o último mês do trimestre
            month = trimester * 3
            # Usar o último dia do mês
            day = 31 if month in [3, 12] else (30 if month in [6, 9] else 28)
            date_str = f"{year}-{month:02d}-{day:02d}"
        else:
            # Se não conseguir extrair a data do nome, usar data atual
            date_str = datetime.now().strftime('%Y-%m-%d')
        
        # Extrair informações das demonstrações contábeis
        for evipnet in root.findall('.//evipnet'):
            for line in evipnet.findall('.//linha'):
                reg_ans = line.find('REG_ANS').text if line.find('REG_ANS') is not None else ''
                cd_conta = line.find('CD_CONTA_CONTABIL').text if line.find('CD_CONTA_CONTABIL') is not None else ''
                descricao = line.find('DESCRICAO').text if line.find('DESCRICAO') is not None else ''
                
                # Tratar valores numéricos
                saldo_inicial = line.find('VL_SALDO_INICIAL').text if line.find('VL_SALDO_INICIAL') is not None else '0'
                saldo_final = line.find('VL_SALDO_FINAL').text if line.find('VL_SALDO_FINAL') is not None else '0'
                
                # Converter valores para formato decimal (substituindo vírgula por ponto)
                saldo_inicial = saldo_inicial.replace('.', '').replace(',', '.')
                saldo_final = saldo_final.replace('.', '').replace(',', '.')
                
                # Adicionar registro
                records.append({
                    'data': date_str,
                    'reg_ans': reg_ans,
                    'cd_conta_contabil': cd_conta,
                    'descricao': descricao,
                    'vl_saldo_inicial': saldo_inicial,
                    'vl_saldo_final': saldo_final
                })
        
        return records
    except Exception as e:
        print(f"Erro ao processar o arquivo {file_path}: {e}")
        return []

def insert_into_postgres(records):
    """Insere os registros processados diretamente no PostgreSQL"""
    # Configuração da conexão
    conn_params = {
        'dbname': 'ans_data',
        'user': 'postgres',
        'password': 'sua_senha',
        'host': 'localhost',
        'port': '5432'
    }
    
    try:
        # Conectar ao banco de dados
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
        
        # Preparar dados para inserção
        columns = ['data', 'reg_ans', 'cd_conta_contabil', 'descricao', 'vl_saldo_inicial', 'vl_saldo_final']
        values = [[record[col] for col in columns] for record in records]
        
        # SQL para inserção em massa
        query = """
            INSERT INTO demonstracoes_contabeis (data, reg_ans, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final)
            VALUES %s
        """
        
        # Executar inserção em massa
        execute_values(cursor, query, values)
        
        # Commit e fechar conexão
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"Inseridos {len(records)} registros com sucesso no PostgreSQL")
    except Exception as e:
        print(f"Erro ao inserir no PostgreSQL: {e}")

def main():
    # Diretório onde estão os arquivos XML
    xml_dir = './dados/demonstracoes_contabeis/'
    
    # Obter todos os arquivos XML dos últimos 2 anos
    # Assumindo que os arquivos seguem um padrão com o ano no nome
    current_year = datetime.now().year
    
    # Padrão para encontrar arquivos dos últimos 2 anos (adapte conforme a nomenclatura real)
    file_pattern_1 = os.path.join(xml_dir, f"*{current_year-2}*.xml")
    file_pattern_2 = os.path.join(xml_dir, f"*{current_year-1}*.xml")
    
    files_year_1 = glob.glob(file_pattern_1)
    files_year_2 = glob.glob(file_pattern_2)
    
    # Combinar todos os arquivos
    all_files = files_year_1 + files_year_2
    
    all_records = []
    
    # Processar cada arquivo
    for file_path in all_files:
        print(f"Processando {file_path}...")
        records = process_xml_file(file_path)
        all_records.extend(records)
    
    # Método 1: Salvar como CSV para importação posterior
    if all_records:
        df = pd.DataFrame(all_records)
        output_file = 'demonstracoes_processadas.csv'
        df.to_csv(output_file, index=False, sep=';')
        print(f"Arquivo {output_file} gerado com sucesso. Total de registros: {len(df)}")
    
    # Método 2: Inserir diretamente no PostgreSQL
    # Descomente para usar este método
    # if all_records:
    #     insert_into_postgres(all_records)

if __name__ == "__main__":
    main()