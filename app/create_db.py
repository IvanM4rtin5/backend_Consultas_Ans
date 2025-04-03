from flask import Flask
from app.config import Config
from app.database import db
from app.models import DemonstracoesContabeis, OperadorasAtivas
from sqlalchemy import text

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def create_database():
    """Cria o banco e as tabelas."""
    with app.app_context():
        db.create_all()

        # Criando índices para melhorar performance
        db.session.execute (text("CREATE INDEX IF NOT EXISTS idx_reg_ans ON demonstracoes_contabeis (reg_ans);"))
        db.session.execute(text("CREATE INDEX IF NOT EXISTS idx_data ON demonstracoes_contabeis (data);"))
        db.session.execute(text("CREATE INDEX IF NOT EXISTS idx_conta ON demonstracoes_contabeis (cd_conta_contabil);"))
        db.session.execute(text("CREATE INDEX IF NOT EXISTS idx_operadoras_reg_ans ON operadoras_ativas (registro_ans);"))
        
        db.session.commit()
        print("✅ Banco de dados e tabelas criados com sucesso!")

if __name__ == '__main__':
    create_database()
    app.run(debug=True, port=5000)