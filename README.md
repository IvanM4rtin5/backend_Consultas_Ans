# 💼 Expense Query API - ANS (National Supplementary Health Agency)

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.3-000000?logo=flask)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-4169E1?logo=postgresql)](https://www.postgresql.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.30-333333?logo=sqlalchemy)](https://www.sqlalchemy.org/)

Backend API for querying healthcare provider expenses, integrated into a relational database with data processed from ANS.

---

## 🧩 Main Features

### **RESTful API**
- Consult the biggest expenses per quarter
- Health check endpoint
- Filtering by operator and period
- Pagination of results
- **Postman queries**

![Image](https://github.com/IvanM4rtin5/backend_Consultas_Ans/blob/main/public/image/consulta_postman.jpeg)

### **Database**
- Optimized modeling for financial queries
- Indexes for performance on large datasets
- Relationship between operators and financial statements
- Data import via CSV
- **Queries in SQL**

![Image](https://github.com/IvanM4rtin5/backend_Consultas_Ans/blob/main/public/image/consulta_sql.png)

---

## 🚀 How to Execute the Project

### Prerequisites
- Python 3.10+
- PostgreSQL 17+
- Postman (for testing endpoints)

### Download csv files from the ans website

1. the user will have to download the csv files from the websites (selecting the year of interest):
  
- https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/
- https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/

2. insert in the **Uploads** folder

### Initial Setup
1. Create a PostgreSQL database:

```sql
CREATE DATABASE my_base;
```
2. Configure the environment variables in .env:

```ini Copy
DB_USER=postgres
DB_PASSWORD=secret_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=my_base
```
**Installation**

```bash Copy
git clone https://github.com/IvanM4rtin5/backend_Consultas_Ans.git
```
```
cd api-ans
```
```
python -m venv venv
```
```
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```
```
pip install -r requirements.txt
```
**Bank Startup**
```bash Copy
python create_db.py # Create tables and indexes
python import_csv.py # Import data from CSVs
```
**Run the API**
```bash Copy
python run.py # Start server at http://localhost:5000
```
## 📡 Main Endpoints
**Health Check**
```http Copy
GET /api/health
```
**Top 10 Expenses from the Last Quarter**
```http Copy
GET /api/expenses/quarter
```
**Sample Answer:**

```json Copy

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
### 🗃️ Project Structure
```Copy
api-ans/
├── app/
│ ├── routes/
│ │ ├── expenses.py   # Query routes
│ │ └── health.py     # Health check
│ ├── __init__.py     # Application factory
│ ├── config.py       # Flask Settings
│ ├── create_db.py    # DB creation script
│ ├── database.py     # Connection to the database
│ ├── models.py       # SQLAlchemy Models
│ └── import_csv.py   # Data importer
├── .env              # Environment variables
├── requirements.txt  # Dependencies
└── run.py            # Entrypoint of the application
```

### 🔍 Example SQL Queries
Query used in the /expenses/quarter endpoint:

```sql Copy

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
### 📌 Usage Tips
Test with Postman: Import the collection available in docs/postman_collection.json

Optimization: Pre-built indexes speed up queries on reg_ans and data

Example Data: CSVs must follow the structure of the accounting_demonstrations and active_operators tables

---
### 📧 Contact

**Developer:** Ivan Martins

***Email:** ivanmarti.alves@gmail.com

**LinkedIn:** https://www.linkedin.com/in/ivan-martins-alves/
