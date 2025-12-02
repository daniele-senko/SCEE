# 🛒 SCEE - Sistema de Comércio Eletrônico

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Tkinter](https://img.shields.io/badge/Interface-Tkinter-green.svg)](https://docs.python.org/3/library/tkinter.html)
[![SQLite](https://img.shields.io/badge/Database-SQLite-orange.svg)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-Pytest-brightgreen.svg)]()

> Um sistema de e-commerce desktop robusto, desenvolvido em Python com arquitetura em camadas e interface gráfica moderna.

---

## 📋 Sobre o Projeto

O **SCEE** é uma aplicação completa de vendas online simulada, construída para demonstrar boas práticas de Engenharia de Software. O projeto foge do básico, implementando padrões de design avançados, persistência de dados real e uma separação clara de responsabilidades.

O sistema atende a dois perfis de usuários distintos: **Clientes** (compra) e **Administradores** (gestão).

## 🚀 Funcionalidades Principais

### 👤 Área do Cliente
- **Autenticação Segura:** Login e Registro com hash de senha (Bcrypt).
- **Catálogo Interativo:** Visualização de produtos com imagens, preços e estoque.
- **Filtros Avançados:** Busca por nome, categoria e faixa de preço.
- **Carrinho de Compras:** Gestão dinâmica de itens e cálculo de subtotal.
- **Checkout Completo:**
  - Cadastro e seleção de múltiplos endereços de entrega.
  - Cálculo de Frete (Simulação de Correios/Transportadora).
  - Pagamento via Cartão de Crédito ou PIX.
- **Histórico de Pedidos:** Acompanhamento de status e detalhes de compras passadas.

### 🛡️ Área Administrativa (Backoffice)
- **Dashboard:** Visão geral com métricas de vendas, total de produtos e pedidos pendentes.
- **Gestão de Produtos:** CRUD completo (Criar, Ler, Atualizar, Deletar) com upload de imagens.
- **Gestão de Categorias:** Organização da loja.
- **Controle de Pedidos:** Visualização de pedidos e atualização de status (Pendente -> Processando -> Enviado -> Entregue).

---

## 🏗️ Arquitetura e Design Patterns

O projeto foi estruturado seguindo princípios de **Clean Architecture** e **SOLID**, garantindo manutenibilidade e testabilidade.

| Padrão / Conceito | Aplicação no Projeto |
|-------------------|----------------------|
| **MVC** | Separação clara entre *Views* (Tkinter), *Controllers* (Fluxo) e *Models* (Dados). |
| **Repository Pattern** | Abstração da camada de dados (`src/repositories`), permitindo trocar o banco sem afetar a lógica. |
| **Service Layer** | Regras de negócio isoladas (`src/services`) para validações, cálculos e orquestração. |
| **Strategy Pattern** | Implementado nos cálculos de frete e gateways de pagamento. |
| **Singleton** | Gerenciamento único da conexão com o banco de dados (`DatabaseConnection`). |
| **Template Method** | Estrutura base para componentes de UI (ex: `BaseCard`). |

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.9+
- **GUI:** Tkinter (Nativo) + Componentes Customizados (Cards, Modais, Toasts)
- **Banco de Dados:** SQLite 3 (Nativo)
- **Segurança:** `bcrypt` e `passlib` para criptografia.
- **Validação:** `email-validator` e Regex para CPF/Dados.
- **Testes:** `pytest`, `pytest-mock` e `coverage`.

---

## ⚡ Instalação e Execução

### Pré-requisitos
- Python 3.9 ou superior instalado.

### Passo a Passo

1. **Clone o repositório:**
```bash
   git clone https://github.com/seu-usuario/SCEE.git
   cd SCEE
````

2.  **Crie e ative um ambiente virtual:**

    ```bash
    # Windows
    python -m venv .venv
    .venv\Scripts\activate

    # Linux/Mac
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute a aplicação:**

    ```bash
    python main.py
    ```

    *Nota: Na primeira execução, o banco de dados `database_sqlite/SCEE.db` será criado e populado automaticamente com dados de exemplo.*

-----

## 🔐 Credenciais de Acesso (Seed Data)

Para testar o sistema, utilize as contas pré-configuradas:

| Perfil | Email | Senha |
|--------|-------|-------|
| **Administrador** | `admin@scee.com` | `admin123` |
| **Cliente** | `joao@email.com` | `cliente123` |

-----

## 🧪 Testes Automatizados

O projeto possui uma suíte de testes abrangente cobrindo Repositórios, Services e Controllers.

Para executar os testes:

```bash
# Executar todos os testes
pytest

# Executar com relatório de cobertura
pytest --cov=src --cov-report=term-missing
```

-----

## 📂 Estrutura de Diretórios

```text
scee/
├── .env
├── .gitignore
├── Classe_UML.webp
├── LICENSE
├── main.py
├── pytest.ini
├── QUICKSTART.md
├── README.md
├── requirements-dev.txt
├── requirements.txt
├── setup.py
├── UML.md
│
├── database_sqlite/
│   └── SCEE.db
│
├── docs/
│   ├── CONTROLLERS.md
│   ├── CREDENCIAIS.md
│   ├── ERRO_X11.md
│   └── POO_CARDS.md
│
├── manuais/
│   └── Usando env.md
│
├── src/
│   ├── config/
│   │   ├── database.py
│   │   ├── database_initializer.py
│   │   ├── database_seeder.py
│   │   └── settings.py
│   │
│   ├── controllers/
│   │   ├── __init__.py
│   │   ├── admin_controller.py
│   │   ├── auth_controller.py
│   │   ├── base_controller.py
│   │   ├── cart_controller.py
│   │   ├── catalog_controller.py
│   │   ├── checkout_controller.py
│   │   └── order_controller.py
│   │
│   ├── integration/
│   │   ├── payment/
│   │   │   ├── credit_card_gateway.py
│   │   │   ├── payment_gateway.py
│   │   │   └── pix_gateway.py
│   │   └── shipping/
│   │       ├── correios_calculator.py
│   │       └── shipping_calculator.py
│   │
│   ├── interfaces/
│   │   └── i_repository.py
│   │
│   ├── models/
│   │   ├── base_model.py
│   │   ├── enums.py
│   │   ├── products/
│   │   │   ├── __init__.py
│   │   │   ├── category_model.py
│   │   │   └── product_model.py
│   │   ├── sales/
│   │   │   ├── cart_item_model.py
│   │   │   └── order_model.py
│   │   └── users/
│   │       ├── address_model.py
│   │       ├── admin_model.py
│   │       ├── client_model.py
│   │       └── user_model.py
│   │
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── address_repository.py
│   │   ├── base_repository.py
│   │   ├── cart_repository.py
│   │   ├── category_repository.py
│   │   ├── client_repository.py
│   │   ├── order_repository.py
│   │   ├── product_repository.py
│   │   └── user_repository.py
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── cart_service.py
│   │   ├── catalog_service.py
│   │   ├── checkout_service.py
│   │   ├── email_service.py
│   │   ├── order_service.py
│   │   └── user_service.py
│   │
│   ├── utils/
│   │   ├── formatters.py
│   │   ├── security/
│   │   │   └── password_hasher.py
│   │   └── validators/
│   │       ├── cpf_validator.py
│   │       ├── email_validator.py
│   │       └── price_validator.py
│   │
│   └── views/
│       ├── main_window.py
│       ├── admin/
│       │   ├── dashboard_view.py
│       │   ├── manage_categories_view.py
│       │   ├── manage_orders_view.py
│       │   ├── manage_products_view.py
│       │   └── product_form_view.py
│       ├── client/
│       │   ├── address_form_view.py
│       │   ├── cart_view.py
│       │   ├── checkout_view.py
│       │   ├── home_view.py
│       │   ├── login_view.py
│       │   ├── my_orders_view.py
│       │   └── register_view.py
│       └── components/
│           ├── __init__.py
│           ├── README.md
│           ├── card.py
│           ├── custom_button.py
│           ├── data_table.py
│           ├── form_field.py
│           ├── modal_message.py
│           ├── order_details_modal.py
│           ├── product_card.py
│           └── product_details_modal.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── README.md
│   ├── repositories/
│   │   ├── test_address_repository.py
│   │   ├── test_cart_repository.py
│   │   ├── test_category_repository.py
│   │   ├── test_client_repository.py
│   │   ├── test_order_repository.py
│   │   ├── test_product_repository.py
│   │   └── test_user_repository.py
│   ├── services/
│   │   ├── test_auth_service.py
│   │   ├── test_cart_service.py
│   │   ├── test_catalog_service.py
│   │   ├── test_email_service.py
│   │   ├── test_order_service.py
│   │   └── test_user_service.py
│   └── test_controllers/
│       ├── __init__.py
│       ├── conftest.py
│       ├── test_admin_controller.py
│       ├── test_auth_controller.py
│       ├── test_cart_controller.py
│       ├── test_catalog_controller.py
│       └── test_order_controller.py
│
└── uploads/
    └── produtos/
        ├── 52392576-1016-4b16-a68e-beff4163f867.webp
        └── 65b10ac0-c1da-4084-bcdf-008f6b21cdcb.png
```

-----

## ⚠️ Solução de Problemas

### Erro X11 (Linux)

Se você estiver usando Linux (especialmente Rocky Linux/RHEL com XFCE) e encontrar o erro `X Error of failed request: BadLength`, o sistema já possui uma mitigação implementada em `main.py` e `src/config/settings.py` usando fontes compatíveis. Consulte `docs/ERRO_X11.md` para mais detalhes.

-----

## 📄 Licença

Distribuído sob a licença BSD 3-Clause. Veja `LICENSE` para mais informações.

-----

<div align="center"\>
Desenvolvido com 💙 pelos alunos de Sistemas de Informação.
</div>


