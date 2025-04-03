from sqlalchemy import Column, Integer, String, Date, Numeric
from app.database import db

class DemonstracoesContabeis(db.Model):
    __tablename__ = "demonstracoes_contabeis"

    id = Column(Integer, primary_key=True, index=True)
    data = Column(Date)
    reg_ans = Column(String(20), index=True)
    cd_conta_contabil = Column(String(20))
    descricao = Column(String(255))
    vl_saldo_inicial = Column(Numeric(15, 2))
    vl_saldo_final = Column(Numeric(15, 2))

class OperadorasAtivas(db.Model):
    __tablename__ = "operadoras_ativas"

    id = Column(Integer, primary_key=True, index=True)
    registro_ans = Column(String(20), index=True)
    cnpj = Column(String(20))
    razao_social = Column(String(255))
    nome_fantasia = Column(String(255))
    modalidade = Column(String(100))
    logradouro = Column(String(255))
    numero = Column(String(20))
    complemento = Column(String(100))
    bairro = Column(String(100))
    cidade = Column(String(100))
    uf = Column(String(2))
    cep = Column(String(10))
    ddd = Column(String(3))
    telefone = Column(String(20))
    fax = Column(String(20))
    endereco_eletronico = Column(String(100))
    representante = Column(String(255))
    cargo_representante = Column(String(100))
    regiao_comercializacao = Column(String(100))
    data_registro_ans = Column(Date)
