from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

# Modelos da Base de Dados (Estrutura da aula)
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

# Criação automática das tabelas ao iniciar
with app.app_context():
    db.create_all()

# Rotas principais
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/produto')
def produto():
    return render_template('produto.html')

@app.route('/carrinho')
def carrinho():
    return render_template('carrinho.html')

if __name__ == "__main__":
    app.run(debug=True)