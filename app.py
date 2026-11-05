from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from config import Config
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

# Modelos da Base de Dados
class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)

class Produto(db.Model):
    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    estoque = db.Column(db.Integer, nullable=False)

class Pedido(db.Model):
    __tablename__ = 'pedidos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    data = db.Column(db.Date)

class ItemPedido(db.Model):
    __tablename__ = 'itens_pedido'
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), primary_key=True)
    quantidade = db.Column(db.Integer, nullable=False)

# Criação automática das tabelas (comentado temporariamente)
# with app.app_context():
#     db.create_all()

# Rotas principais (usando as variáveis do Config)
@app.route(Config.ROUTE_HO)
def home():
    return render_template('index.html', Config=Config)

@app.route(Config.ROUTE_PROD)
def produto():
    return render_template('produto.html', Config=Config)

@app.route(Config.ROUTE_CAR)
def carrinho():
    return render_template('carrinho.html', Config=Config)

@app.route(Config.ROUTE_ADMIN, methods=['GET', 'POST'])
def admin():
    # Se o admin submeter um novo produto pelo formulário
    if request.method == 'POST':
        nome = request.form.get('nome')
        preco = request.form.get('preco')
        estoque = request.form.get('estoque')
        
        if nome and preco and estoque:
            try:
                novo_produto = Produto(nome=nome, preco=float(preco), estoque=int(estoque))
                db.session.add(novo_produto)
                db.session.commit()
            except Exception as e:
                print(f"Erro ao salvar no banco: {e}")
                db.session.rollback()
            
            # Redirecionamento correto para a rota admin
            return redirect(Config.ROUTE_ADMIN)

    # Tentativa de buscar dados do PostgreSQL com segurança (evita travamentos infinitos)
    try:
        total_usuarios = Cliente.query.count()
        produtos_cadastrados = Produto.query.all()
        total_stock = db.session.query(db.func.sum(Produto.estoque)).scalar() or 0
    except Exception as e:
        print(f"Aviso: Banco de dados indisponível ({e}). Usando dados temporários.")
        total_usuarios = 0
        produtos_cadastrados = []
        total_stock = 0

    stats = {
        "total_vendas": "R$ 0,00",
        "total_usuarios": total_usuarios,
        "produtos_em_stock": total_stock,
        "descontos_ativos": 0
    }
    
    return render_template('admin.html', stats=stats, produtos=produtos_cadastrados, Config=Config)

# Rota para deletar produto diretamente no banco
@app.route(Config.ROUTE_B, methods=['POST'])
def deletar_produto(id):
    produto = Produto.query.get_or_404(id)
    db.session.delete(produto)
    db.session.commit()
    return redirect(url_for(Config.ROUTE_ADMIN))

if __name__ == "__main__":
    app.run(debug=True)