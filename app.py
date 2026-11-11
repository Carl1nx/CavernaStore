from flask import Flask, render_template, redirect, url_for, request, session
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

# Rotas principais
@app.route(Config.ROUTE_HO)
def home():
    produtos = Produto.query.all()  
    return render_template('index.html', produtos=produtos, Config=Config)

@app.route(Config.ROUTE_PROD)
def produto():
    return render_template('produto.html', Config=Config)

@app.route(Config.ROUTE_CAR)
def carrinho():
    produto_ids = session.get('carrinho', [])
    produtos_no_carrinho = Produto.query.filter(Produto.id.in_(produto_ids)).all() if produto_ids else []
    return render_template('carrinho.html', produtos=produtos_no_carrinho, Config=Config)

@app.route('/adicionar-carrinho/<int:produto_id>', methods=['POST'])
def adicionar_carrinho(produto_id):
    if 'carrinho' not in session:
        session['carrinho'] = []
    session['carrinho'].append(produto_id)
    session.modified = True
    return redirect(url_for('carrinho'))

@app.route(Config.ROUTE_ADMIN, methods=['GET', 'POST'])
def admin():
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
            
        return redirect(Config.ROUTE_ADMIN)

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
@app.route('/admin/produto/deletar/<int:produto_id>', methods=['POST'])
def deletar_produto(produto_id):
    produto_obj = Produto.query.get_or_404(produto_id)
    db.session.delete(produto_obj)
    db.session.commit()
    return redirect(Config.ROUTE_ADMIN)

# Rota para relatórios escolares (clientes, mangas compradas e total gasto)
@app.route('/admin/relatorios')
def relatorios_clientes():
    try:
        relatorio_clientes = db.session.query(
            Cliente.id,
            Cliente.nome,
            Cliente.cidade,
            db.func.count(db.distinct(Pedido.id)).label('total_pedidos'),
            db.func.coalesce(db.func.sum(ItemPedido.quantidade), 0).label('total_mangas'),
            db.func.coalesce(db.func.sum(ItemPedido.quantidade * Produto.preco), 0).label('total_gasto')
        ).outerjoin(Pedido, Cliente.id == Pedido.cliente_id)\
         .outerjoin(ItemPedido, Pedido.id == ItemPedido.pedido_id)\
         .outerjoin(Produto, ItemPedido.produto_id == Produto.id)\
         .group_by(Cliente.id, Cliente.nome, Cliente.cidade).all()

        detalhes_pedidos = db.session.query(
            Pedido.id.label('pedido_id'),
            Cliente.nome.label('cliente_nome'),
            Pedido.data,
            db.func.sum(ItemPedido.quantidade * Produto.preco).label('valor_pedido')
        ).join(Cliente, Pedido.cliente_id == Cliente.id)\
         .join(ItemPedido, Pedido.id == ItemPedido.pedido_id)\
         .join(Produto, ItemPedido.produto_id == Produto.id)\
         .group_by(Pedido.id, Cliente.nome, Pedido.data).all()

    except Exception as e:
        print(f"Erro ao gerar relatórios: {e}")
        relatorio_clientes = []
        detalhes_pedidos = []

    return render_template(
        'relatorios.html', 
        relatorio_clientes=relatorio_clientes, 
        detalhes_pedidos=detalhes_pedidos, 
        Config=Config
    )

if __name__ == "__main__":
    app.run(debug=True)