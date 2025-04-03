import os
import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
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
                    df.columns = df.columns.str.lower()

                    # Substituir NaN por None
                    df = df.where(pd.notna(df), None)

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

                    print(f"📦 Tamanho do DataFrame: {df.shape[0]} linhas x {df.shape[1]} colunas")

                    if "reg_ans" in df.columns:
                        importar_demonstracoes(df)
                    elif "registro_ans" in df.columns:
                        importar_operadoras(df)
                    else:
                         print(f"⚠️ Estrutura inesperada no arquivo {file}: {df.columns.tolist()}")

                except Exception as e:
                    print(f"❌ Erro ao processar {file}: {e}")

def importar_demonstracoes(df):
    """Importa os dados de demonstrações contábeis do DataFrame para o banco."""

    df["data"] = pd.to_datetime(df["data"], format="%Y-%m-%d", errors="coerce")
    df["data"] = df["data"].where(pd.notna(df["data"]), None)

    for _, row in df.iterrows():
        reg_ans = str(row.get("reg_ans")) if row.get("reg_ans") is not None else None
        cd_conta_contabil = str(row.get("cd_conta_contabil")) if row.get("cd_conta_contabil") is not None else None

        existe = session.query(DemonstracoesContabeis).filter_by(
            data=row.get("data"),
            reg_ans=reg_ans,
            cd_conta_contabil=cd_conta_contabil
        ).first()

        if not existe:  
            demo = DemonstracoesContabeis(
                data=row.get("data"),
                reg_ans=reg_ans,
                cd_conta_contabil=cd_conta_contabil,
                descricao=row.get("descricao"),
                vl_saldo_inicial=row.get("vl_saldo_inicial"),
                vl_saldo_final=row.get("vl_saldo_final")
            )
            session.add(demo)
    
    try:
        session.commit()
        print("✅ Dados de demonstrações contábeis importados com sucesso!")
    except IntegrityError as e:
        session.rollback()
        print(f"⚠️ Erro de integridade: {e}")
    finally: 
        session.close()

def importar_operadoras(df):
    """Importa os dados das operadoras ativas do DataFrame para o banco."""

    df.columns = df.columns.str.lower()  # Padroniza os nomes das colunas
    df["data_registro_ans"] = pd.to_datetime(df["data_registro_ans"], format="%Y-%m-%d", errors="coerce")

    for _, row in df.iterrows():
        operadora = OperadorasAtivas(
            registro_ans=row.get("registro_ans"),
            cnpj=row.get("cnpj"),
            razao_social=row.get("razao_social"),
            nome_fantasia=row.get("nome_fantasia"),
            modalidade=row.get("modalidade"),
            logradouro=row.get("logradouro"),
            numero=row.get("numero"),
            complemento=row.get("complemento"),
            bairro=row.get("bairro"),
            cidade=row.get("cidade"),
            uf=row.get("uf"),
            cep=row.get("cep"),
            ddd=row.get("ddd"),
            telefone=row.get("telefone"),
            fax=row.get("fax"),
            endereco_eletronico=row.get("endereco_eletronico"),
            representante=row.get("representante"),
            cargo_representante=row.get("cargo_representante"),
            regiao_comercializacao=row.get("regiao_comercializacao"),
            data_registro_ans=row.get("data_registro_ans"),
        )
        session.add(operadora)

    try:
        session.commit()
        print("✅ Dados das operadoras ativas importados com sucesso!")
    except IntegrityError as e:
        session.rollback()
        print(f"⚠️ Erro de integridade: {e}")
    finally: 
        session.close()

if __name__ == "__main__":
    importar_arquivos()
