# 💼 API de Consulta de Despesas - ANS (Agência Nacional de Saúde Suplementar)

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.3-000000?logo=flask)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-4169E1?logo=postgresql)](https://www.postgresql.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.30-333333?logo=sqlalchemy)](https://www.sqlalchemy.org/)

API backend para consulta de despesas de operadoras de saúde, integrada a um banco de dados relacional com dados processados da ANS.

---

## 🛠️ Tecnologias Utilizadas

<div align="left">
  <img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Flask-000000?logo=flask" alt="Flask" />
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql" alt="PostgreSQL" />
  <img src="https://img.shields.io/badge/SQLAlchemy-333333?logo=sqlalchemy" alt="SQLAlchemy" />
  <img src="https://img.shields.io/badge/pandas-150458?logo=pandas" alt="Pandas" />
  <img src="https://img.shields.io/badge/Postman-FF6C37?logo=postman" alt="Postman" />
</div>

---

## 🧩 Funcionalidades Principales

### **API RESTful**
- Consulta das maiores despesas por trimestre
- Endpoint de health check
- Filtragem por operadora e período
- Paginação de resultados

### **Banco de Dados**
- Modelagem otimizada para consultas financeiras
- Índices para performance em grandes datasets
- Relação entre operadoras e demonstrações contábeis
- Importação de dados via CSV

---

## 🚀 Como Executar o Projeto

### Pré-requisitos
- Python 3.10+
- PostgreSQL 17+
- Postman (para testar endpoints)

### Configuração Inicial
1. Crie um banco PostgreSQL:

```sql
CREATE DATABASE minha_base;
```
2. Configure as variáveis de ambiente no .env:

ini
Copy
DB_USER=postgres
DB_PASSWORD=senha_secreta
DB_HOST=localhost
DB_PORT=5432
DB_NAME=minha_base

**Instalação**

```bash
Copy
git clone https://github.com/seu-usuario/api-ans.git
cd api-ans
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
pip install -r requirements.txt
```
**Inicialização do Banco**
```bash
Copy
python create_db.py  # Cria tabelas e índices
python import_csv.py  # Importa dados dos CSVs
```
**Executar a API**
```bash
Copy
python run.py  # Inicia servidor em http://localhost:5000
```
## 📡 Endpoints Principales
**Health Check**
```http
Copy
GET /api/health
```
**Top 10 Despesas do Último Trimestre**
```http
Copy
GET /api/despesas/trimestre
```
**Resposta de Exemplo:**

```json
Copy
{
  "status": "success",
  "data": [
    {
      "razao_social": "SUL AMERICA COMPANHIA DE SEGURO SAÚDE",
      "registro_ans": "6246",
      "modalidade": "Segquadora Especializada em Saúde",
      "total_despesas": "42249880884.69"
    }
  ]
}
```
### 🗃️ Estrutura do Projeto
```Copy
api-ans/
├── app/
│   ├── routes/
│   │   ├── despesas.py    # Rotas de consulta
│   │   └── health.py      # Health check
│   ├── __init__.py        # Factory da aplicação
│   ├── config.py          # Configurações do Flask
│   ├── create_db.py       # Script de criação do DB
│   ├── database.py        # Conexão com o banco
│   ├── models.py          # Modelos SQLAlchemy
│   └── import_csv.py      # Importador de dados
├── .env                   # Variáveis de ambiente
├── requirements.txt       # Dependências
└── run.py                 # Entrypoint da aplicação
```
### 🔍 Consultas SQL Exemplo
Consulta utilizada no endpoint /despesas/trimestre:

```sql
Copy
WITH UltimoTrimestre AS (
  SELECT MAX(data) AS data_max FROM demonstracoes_contabeis
)
SELECT 
  o.razao_social, 
  o.registro_ans, 
  o.modalidade,
  ABS(SUM(d.vl_saldo_final)) AS total_despesas
FROM demonstracoes_contabeis d
JOIN operadoras_ativas o ON d.reg_ans = o.registro_ans
JOIN UltimoTrimestre ut ON d.data = ut.data_max
WHERE d.descricao LIKE '%ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR%'
GROUP BY o.razao_social, o.registro_ans, o.modalidade
ORDER BY total_despesas DESC
LIMIT 10;
```
### 📌 Dicas de Uso
Teste com Postman: Importe a collection disponível em docs/postman_collection.json

Otimização: Índices pré-criados aceleram consultas em reg_ans e data

Dados de Exemplo: CSVs devem seguir estrutura das tabelas demonstracoes_contabeis e operadoras_ativas

---
### 📧 Contato

**Desenvolvedor:** Ivan Martins
***Email:** ivanmarti.alves@gmail.com
**LinkedIn:** https://www.linkedin.com/in/ivan-martins-alves/
