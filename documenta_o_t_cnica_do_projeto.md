# 📑 Documentação Técnica — CavernaStore

---

## 1. Visão Geral do Sistema

O **CavernaStore** é uma plataforma web de e-commerce e gestão especializada na venda de mangás. O sistema foi desenvolvido utilizando a microframework **Flask (Python)** para o backend, **PostgreSQL** para a gestão e persistência de dados relacionais e **Jinja2 + CSS3 (Modern Dark Theme)** para a renderização do frontend.

---

## 2. Arquitetura da Aplicação

O projeto segue a arquitetura **MVC (Model-View-Controller)** adaptada para Flask:

* **Model (Modelo):** Gerido pelo **SQLAlchemy ORM**, responsável pelo mapeamento relacional de dados para o PostgreSQL (`Cliente`, `Produto`, `Pedido`, `ItemPedido`).
* **View (Visão):** Modelos HTML5 com motor **Jinja2** e folha de estilos modular em `static/css/style.css`.
* **Controller (Controlador):** Rotas definidas no `app.py` que controlam a lógica de negócio, interações de sessão do carrinho e acessos às páginas.

---

## 3. Modelo de Dados (PostgreSQL)

O banco de dados PostgreSQL foi estruturado com integridade referencial para suportar operações de e-commerce.

### 🔹 Principais Entidades:

1. **`cliente`**
   * `id`: Chave Primária (Serial)
   * `nome`: String
   * `email`: String (Único)

2. **`produto` (Mangá)**
   * `id`: Chave Primária (Serial)
   * `nome`: String (Ex: "Berserk Vol. 3")
   * `preco`: Numeric/Float
   * `estoque`: Integer

3. **`pedido`**
   * `id`: Chave Primária (Serial)
   * `data_pedido`: Datetime
   * `cliente_id`: Chave Estrangeira (`cliente.id`)

4. **`item_pedido`**
   * `id`: Chave Primária (Serial)
   * `pedido_id`: Chave Estrangeira (`pedido.id`)
   * `produto_id`: Chave Estrangeira (`produto.id`)
   * `quantidade`: Integer
   * `preco_unitario`: Numeric

---

## 4. Scripts de Automação e Utilitários

### 🛠️ `popular_massa.py`
Script de povoamento em massa desenvolvido para popular a base de dados PostgreSQL com dezenas de registos de teste (produtos, clientes e históricos de compras), permitindo testar o desempenho do sistema sob volume real de dados.

### 🖼️ `baixar_capas.py`
Script de automação que processa todos os produtos registados no PostgreSQL e gera/associa capas individuais em formato JPG (`static/img/mangas/manga_{id}.jpg`), garantindo um catálogo visualmente uniforme e sem falhas de carregamento remoto.

---

## 5. Rotas e Endpoints da Aplicação

| Rota | Método | Descrição |
| :--- | :--- | :--- |
| `/` | `GET` | Página principal com catálogo dinâmico de produtos (grid). |
| `/adicionar_carrinho/<id>` | `POST` | Adiciona um volume específico de mangá à sessão do carrinho. |
| `/carrinho` | `GET` | Visualização dos itens adicionados e resumo de valores. |
| `/admin` | `GET` | Painel administrativo e relatórios de vendas. |

---

## 6. Design System e Interface UI/UX

* **Grid Responsiva:** O catálogo utiliza CSS Grid (`repeat(auto-fill, minmax(220px, 1fr))`) para se adaptar automaticamente a smartphones, tablets e desktops.
* **Paleta Dark Theme:** Desenvolvida com variáveis CSS para fácil manutenção (`--bg-color: #121214`, `--card-bg: #1e1e24`, `--primary-color: #8257e5`).
* **Tratamento de Fallbacks:** Caso uma capa local seja removida, o atributo `onerror` do HTML redireciona para um elemento placeholder estilizado, mantendo a estabilidade visual da loja.

---

## 7. Roteiro para Apresentação Escolar / Demonstração

1. **Introdução:** Apresentar a proposta do CavernaStore (Loja temática de mangás).
2. **PostgreSQL:** Demonstrar a estrutura das tabelas no pgAdmin / VS Code e destacar a povoação em massa efetuada.
3. **Navegação Web:** Mostrar a vitrine em tema escuro, a resposta interativa da grelha de produtos e a sincronização das capas por ID.
4. **Carrinho:** Demonstrar a adição de um produto e o contador dinâmico na navbar.
5. **Considerações Finais:** Destacar a estabilidade do código, modularidade do CSS e automação através de scripts Python.