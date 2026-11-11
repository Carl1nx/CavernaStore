# 📚 CavernaStore

Sistema web completo de e-commerce e gestão de mangás desenvolvido em **Python (Flask)** com persistência de dados em **PostgreSQL**, estruturado com um design moderno em tema escuro e carregamento dinâmico de recursos visuais.

---

## 🚀 Funcionalidades Principais

* **Catálogo Dinâmico em Grelha:** Vitrine moderna organizada com CSS Grid (`product-grid`), exibindo capas personalizadas, preços formatados e controlo de stock em tempo real.
* **Gestão de Capas por ID:** Sistema automatizado que associa imagens de capa individuais a cada mangá através do seu identificador único na base de dados (`manga_{id}.jpg`).
* **Carrinho de Compras Interativo:** Gestão de itens em sessão com contador dinâmico de produtos adicionados.
* **Painel Administrativo:** Acesso direto a ferramentas de gestão e relatórios de backend.
* **Base de Dados Robusta:** Populada em massa com dezenas de registos de clientes, mangás, pedidos e itens através de scripts dedicados.

---

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python, Flask, SQLAlchemy, PostgreSQL
* **Frontend:** HTML5, CSS3 (Custom Properties, Flexbox, CSS Grid, Tema Escuro)
* **Gestão de Dependências:** `pip`, Ambiente Virtual (`.venv`)
* **Utilitários:** Scripts Python customizados para população de massa e geração de recursos visuais.

---

## 📂 Estrutura do Projeto

```text
CavernaStore/
│
├── static/
│   ├── css/
│   │   └── style.css          # Folha de estilos moderna (Tema escuro & Grid)
│   └── img/
│       └── mangas/            # Capas dos mangás organizadas por ID (manga_{id}.jpg)
│
├── templates/
│   └── index.html             # Página principal do catálogo (Jinja2)
│
├── app.py                     # Aplicação principal Flask e rotas
├── popular_massa.py           # Script de povoamento em massa da BD
├── baixar_capas.py            # Script de geração/associação de capas locais
└── README.md                  # Documentação do projeto
