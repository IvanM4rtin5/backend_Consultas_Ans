import os
import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy import cast , Date
from unidecode import unidecode
from app.database import engine
from app.models import DemonstracoesContabeis, OperadorasAtivas

UPLOADS_DIR = "uploads"

Session = sessionmaker(bind=engine)
session = Session()

def importar_arquivos():
    """Importa os dados de todos os arquivos CSV dentro de uploads."""
    
    for root, _, files in os.walk(UPLOADS_DIR):
        for file in files:
            if file.endswith(".csv"):
                file_path = os.path.join(root, file)
                print(f"📂 Processando arquivo: {file_path}")

                try:
                    df = pd.read_csv(file_path, delimiter=";", encoding="utf-8")
                    df.columns = [unidecode(col).lower().strip().replace(" ", "_") for col in df.columns]
                    df = df.where(pd.notna(df), None)

                    print(f"📦 Tamanho do DataFrame: {df.shape[0]} linhas x {df.shape[1]} colunas")
                    print(f"📋 Colunas encontradas: {df.columns.tolist()}")

                    if "reg_ans" in df.columns and "vl_saldo_inicial" in df.columns:
                        # Converter campos numéricos para demonstrações contábeis
                        print("🔍 Identificado como arquivo de demonstrações contábeis")
                        
                        df["vl_saldo_inicial"] = (
                            df["vl_saldo_inicial"]
                            .astype(str)
                            .str.replace(".", "", regex=False)
                            .str.replace(",", ".", regex=False)
                            .astype(float)
                        )
                        df["vl_saldo_final"] = (
                            df["vl_saldo_final"]
                            .astype(str)
                            .str.replace(".", "", regex=False)
                            .str.replace(",", ".", regex=False)
                            .astype(float)
                        )
                        
                        df["data"] = pd.to_datetime(df["data"], errors="coerce")
                        df = df.dropna(subset=["data"])
                        
                        importar_demonstracoes(df)
                    elif "registro_ans" in df.columns or "razao_social" in df.columns:
                        print("🔍 Identificado como arquivo de operadoras")
                        
                        # Ajustar nome da coluna se necessário 
                        if "regiao_de_comercializacao" in df.columns:
                            df.rename(columns={"regiao_de_comercializacao": "regiao_comercializacao"}, inplace=True)
                            
                        importar_operadoras(df)
                    else:
                        print(f"⚠️ Estrutura inesperada no arquivo {file}: {df.columns.tolist()}")

                except Exception as e:
                    print(f"❌ Erro ao processar {file}: {str(e)}")
                    import traceback
                    traceback.print_exc()

def importar_demonstracoes(df):
    """Importa os dados de demonstrações contábeis do DataFrame para o banco."""
    print("🚀 Iniciando importação de demonstrações contábeis...")

    session=Session()

    df["data"] = pd.to_datetime(df["data"], format="%Y-%m-%d", errors="coerce").dt.date
    df = df.dropna(subset=["data"])
    df["reg_ans"] = df["reg_ans"].astype(str)
    df["cd_conta_contabil"] = df["cd_conta_contabil"].astype(str)

    registros_existentes = {
        (data, reg_ans, cd_conta_contabil)
        for data, reg_ans, cd_conta_contabil in session.query(
            DemonstracoesContabeis.data, 
            DemonstracoesContabeis.reg_ans,
            DemonstracoesContabeis.cd_conta_contabil
        ).all()
    }

    print(f"📋 {len(registros_existentes)} registros já existem no banco.")

    novos_registros = []
    for _, row in df.iterrows():
        chave = (str(row["data"]), row["reg_ans"], row["cd_conta_contabil"])
        if chave not in registros_existentes:
            novos_registros.append(
                DemonstracoesContabeis(
                    data=row["data"],
                    reg_ans=row["reg_ans"],
                    cd_conta_contabil=row["cd_conta_contabil"],
                    descricao=row["descricao"],
                    vl_saldo_inicial=row["vl_saldo_inicial"],
                    vl_saldo_final=row["vl_saldo_final"],
                )
            )

    print(f"🧹 Filtrados {len(df) - len(novos_registros)} registros já existentes. Restam {len(novos_registros)} novos para importar.")

    try:
        if novos_registros:
            session.bulk_save_objects(novos_registros)
            session.commit()
            print("✅ Dados de demonstrações contábeis importados com sucesso!")
        else:
            print("⚠️ Nenhum novo dado para importar.")
    except IntegrityError as e:
        session.rollback()
        print(f"❌ Erro ao importar dados de demonstrações contábeis: {e}")
    finally:
        session.close()

def importar_operadoras(df):
    """Importa os dados das operadoras ativas do DataFrame para o banco."""
    print("🚀 Iniciando importação de operadoras ativas...")

    session=Session()

    df.columns = df.columns.str.lower()  
    df["data_registro_ans"] = pd.to_datetime(df["data_registro_ans"], format="%Y-%m-%d", errors="coerce")
    df["registro_ans"] = df["registro_ans"].astype(str)
    df["uf"] = df["uf"].astype(str).str[:2] 
    df["ddd"] = df["ddd"].astype(str).str[:3] 

    print("🔎 Verificando registros existentes no banco...")

    registros_existentes = {
        row.registro_ans for row in session.query(OperadorasAtivas.registro_ans).all()
    }

    print(f"📋 {len(registros_existentes)} registros já existem no banco.")

    novos_registros = []
    for _, row in df.iterrows():
        if row["registro_ans"] not in registros_existentes:
            novos_registros.append(
                OperadorasAtivas(
                    registro_ans=row["registro_ans"],
                    cnpj=row["cnpj"],
                    razao_social=row["razao_social"],
                    modalidade=row["modalidade"],
                    logradouro=row["logradouro"],
                    numero=row["numero"],
                    bairro=row["bairro"],
                    cidade=row["cidade"],
                    uf=row["uf"], 
                    cep=row["cep"],
                    ddd=row["ddd"],  
                    telefone=row["telefone"],
                    fax=row["fax"],
                    endereco_eletronico=row["endereco_eletronico"],
                    representante=row["representante"],
                    cargo_representante=row["cargo_representante"],
                    regiao_comercializacao=row["regiao_comercializacao"],
                    data_registro_ans=row["data_registro_ans"],
                )
            )

    print(f"🧹 Filtrados {len(df) - len(novos_registros)} registros já existentes. Restam {len(novos_registros)} novos para importar.")

    try:
        if novos_registros:
            session.bulk_save_objects(novos_registros)
            session.commit()
            print("✅ Dados de operadoras importados com sucesso!")
        else:
            print("⚠️ Nenhum novo dado para importar.")
    except IntegrityError as e:
        session.rollback()
        print(f"❌ Erro ao importar dados de operadoras: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    importar_arquivos()
