# 🛒 SCEE - Sistema de Comércio Eletrônico

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![SQLite](https://img.shields.io/badge/SQLite-3-orange.svg)](https://www.sqlite.org/)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)](https://docs.python.org/3/library/tkinter.html)
[![Tests](https://img.shields.io/badge/Tests-112_passing-brightgreen.svg)]()
[![License](https://img.shields.io/badge/License-Academic-red.svg)]()

> Sistema completo de e-commerce desktop com interface gráfica moderna e arquitetura robusta

## 📋 Sobre o Projeto

SCEE é uma plataforma completa de comércio eletrônico desenvolvida em Python, com foco em arquitetura limpa e experiência do usuário. O projeto implementa:

- ✅ **Interface Desktop Moderna** com Tkinter e componentes reutilizáveis
- ✅ **Banco de Dados SQLite** (zero configuração, sem dependências externas)
- ✅ **Arquitetura em Camadas** (Repository Pattern, Service Layer, MVC)
- ✅ **Autenticação Segura** com bcrypt/passlib
- ✅ **Sistema de Pagamento** (PIX, Cartão de Crédito)
- ✅ **Cálculo de Frete** (Correios, Transportadora)
- ✅ **Gestão Completa** de produtos, categorias, pedidos e usuários
- ✅ **112 Testes Automatizados** com 100% de cobertura backend

## 🚀 Quick Start

```bash
# 1. Clonar repositório
git clone https://github.com/daniele-senko/SCEE.git
cd SCEE

# 2. Criar ambiente virtual
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Executar aplicação
python main.py
```

✨ **Pronto!** Na primeira execução, o banco de dados SQLite será criado automaticamente com dados de exemplo.

### 🔐 Credenciais de Teste

**Área do Cliente:**
- Email: `cliente@scee.com`
- Senha: `cliente123`

**Área Administrativa:**
- Email: `admin@scee.com`
- Senha: `admin123`

## 📁 Estrutura do Projeto

```
SCEE/
├── main.py                          # Ponto de entrada da aplicação
├── requirements.txt                 # Dependências Python
├── database_sqlite/
│   └── scee_loja.db                # Banco SQLite (criado automaticamente)
│
├── src/
│   ├── models/                     # Modelos de dados
│   │   ├── products/               # Produto, Categoria, Imagem
│   │   ├── sales/                  # Carrinho, Pedido, Items
│   │   └── users/                  # Usuário, Cliente, Admin, Endereço
│   │
│   ├── repositories/               # Camada de acesso a dados
│   │   ├── base_repository.py     # Repository Pattern base
│   │   ├── product_repository.py
│   │   ├── cart_repository.py
│   │   ├── order_repository.py
│   │   └── user_repository.py
│   │
│   ├── services/                   # Lógica de negócio
│   │   ├── auth_service.py        # Autenticação e registro
│   │   ├── catalog_service.py     # Catálogo de produtos
│   │   ├── cart_service.py        # Carrinho de compras
│   │   ├── checkout_service.py    # Finalização de pedido
│   │   ├── order_service.py       # Gestão de pedidos
│   │   ├── admin_service.py       # Operações administrativas
│   │   └── strategies/            # Strategy Pattern
│   │       ├── freight_correios.py
│   │       ├── freight_transportadora.py
│   │       ├── payment_credit_card.py
│   │       └── payment_pix.py
│   │
│   ├── views/                      # Interface Tkinter
│   │   ├── main_window.py         # Janela principal e roteamento
│   │   ├── client/                # Área do cliente
│   │   │   ├── login_view.py
│   │   │   ├── register_view.py
│   │   │   ├── home_view.py
│   │   │   ├── cart_view.py
│   │   │   ├── checkout_view.py
│   │   │   └── my_orders_view.py
│   │   ├── admin/                 # Área administrativa
│   │   │   ├── dashboard_view.py
│   │   │   ├── manage_products_view.py
│   │   │   ├── manage_categories_view.py
│   │   │   ├── manage_orders_view.py
│   │   │   └── product_form_view.py
│   │   └── components/            # Componentes reutilizáveis
│   │       ├── custom_button.py
│   │       ├── modal_message.py
│   │       ├── nav_bar.py
│   │       └── product_card.py
│   │
│   ├── utils/                      # Utilitários
│   │   ├── formatters.py
│   │   ├── validators/            # Validações
│   │   │   ├── cpf_validator.py
│   │   │   ├── email_validator.py
│   │   │   └── price_validator.py
│   │   └── security/              # Segurança
│   │       └── password_hasher.py
│   │
│   └── config/                     # Configurações
│       ├── database.py            # Conexão SQLite
│       └── settings.py            # Configurações gerais
│
├── schema/                         # Estrutura do banco
│   ├── schema.sql                 # DDL completo
│   └── triggers.sql               # Triggers e validações
│
├── seed/
│   └── seed.sql                   # Dados iniciais
│
├── tests/                          # Testes (112 testes)
│   ├── test_models/
│   ├── test_repositories/
│   ├── test_services/
│   └── test_utils/
│
└── docs/                           # Documentação
    ├── INSTALACAO.md
    ├── UML.md
    └── ERRO_X11.md
```

## 🎯 Funcionalidades

### 👤 Área do Cliente

- [x] **Autenticação**
  - Login com email/senha
  - Registro de novos clientes
  - Validação de CPF e email
  - Hash seguro de senhas (bcrypt)

- [x] **Catálogo de Produtos**
  - Listagem de produtos por categoria
  - Busca e filtros
  - Visualização detalhada com imagens
  - Produtos relacionados

- [x] **Carrinho de Compras**
  - Adicionar/remover produtos
  - Ajustar quantidades
  - Validação de estoque
  - Cálculo de totais

- [x] **Checkout**
  - Seleção de endereço de entrega
  - Cálculo de frete (Correios/Transportadora)
  - Escolha de método de pagamento (PIX/Cartão)
  - Confirmação de pedido

- [x] **Meus Pedidos**
  - Histórico completo
  - Detalhes de cada pedido
  - Rastreamento de status
  - Nota fiscal virtual

### 👨‍💼 Área Administrativa

- [x] **Dashboard**
  - Estatísticas gerais
  - Resumo de vendas
  - Produtos mais vendidos
  - Pedidos recentes

- [x] **Gestão de Produtos**
  - CRUD completo
  - Upload de imagens
  - Controle de estoque
  - Categorização
  - Ativação/desativação

- [x] **Gestão de Categorias**
  - Adicionar/editar categorias
  - Associar produtos
  - Ativar/desativar

- [x] **Gestão de Pedidos**
  - Visualização de todos os pedidos
  - Atualização de status
  - Detalhes completos
  - Filtros e busca

### 🔧 Recursos Técnicos

- [x] **Repository Pattern** - Abstração de acesso a dados
- [x] **Service Layer** - Lógica de negócio isolada
- [x] **Strategy Pattern** - Frete e pagamento plugáveis
- [x] **Singleton Pattern** - Conexão única com banco
- [x] **MVC Pattern** - Separação de responsabilidades
- [x] **Triggers de Banco** - Validações automáticas
- [x] **Views Materializadas** - Queries otimizadas
- [x] **Componentes Reutilizáveis** - DRY principle
- [x] **Validadores** - CPF, email, preço, estoque
- [x] **Formatadores** - CEP, CPF, moeda, telefone

## 🛠️ Tecnologias

### Core
- **Python 3.9+** - Linguagem principal
- **SQLite 3** - Banco de dados embutido (zero configuração)
- **Tkinter** - Interface gráfica nativa multiplataforma

### Segurança
- **bcrypt 4.1.1** - Hash de senhas
- **passlib 1.7.4** - Gerenciamento de senhas
- **cryptography 41.0.7** - Criptografia adicional

### Validação e Processamento
- **email-validator 2.1.0** - Validação de emails
- **Pillow 10.1.0** - Processamento de imagens
- **python-dotenv 1.0.0** - Variáveis de ambiente

### Testes
- **pytest 7.4.3** - Framework de testes
- **pytest-cov 4.1.0** - Cobertura de código
- **pytest-mock 3.12.0** - Mocks e fixtures
- **coverage 7.3.2** - Relatórios de cobertura

### ORM e Database
- **SQLAlchemy 2.0.23** - ORM (opcional, usado em alguns módulos)
- **PyMySQL 1.1.0** - Driver MySQL (alternativa ao SQLite)

## 📊 Banco de Dados

### SQLite - Zero Configuração

O projeto utiliza **SQLite**, um banco de dados leve e sem necessidade de servidor. 

- 📁 Localização: `database_sqlite/scee_loja.db`
- 🚀 Criação automática na primeira execução
- 💾 Arquivo único, fácil backup
- 🔄 Dados de exemplo pré-carregados

### Schema Completo

**11 Tabelas Principais:**

| Tabela | Descrição | Campos Principais |
|--------|-----------|-------------------|
| `usuarios` | Dados gerais de usuários | id, email, senha_hash, tipo |
| `clientes_info` | Informações específicas de clientes | usuario_id, nome, cpf, telefone |
| `administradores` | Informações específicas de admins | usuario_id, nome, cargo |
| `enderecos` | Endereços de entrega | id, usuario_id, cep, logradouro, cidade, uf |
| `categorias` | Categorias de produtos | id, nome, descricao, ativo |
| `produtos` | Catálogo de produtos | id, nome, preco, estoque, categoria_id |
| `imagens_produto` | Imagens dos produtos | id, produto_id, url, principal |
| `carrinhos` | Carrinhos de compra | id, usuario_id, criado_em |
| `itens_carrinho` | Items do carrinho | id, carrinho_id, produto_id, quantidade |
| `pedidos` | Pedidos realizados | id, cliente_id, total, status, forma_pag |
| `itens_pedido` | Items dos pedidos | id, pedido_id, produto_id, quantidade, preco |

### Views Otimizadas

```sql
-- Produtos completos com categoria e imagens
vw_produtos_completos

-- Clientes com dados completos
vw_clientes_completos

-- Pedidos com todos os detalhes
vw_pedidos_detalhados

-- Carrinhos com valor total calculado
vw_carrinhos_totais
```

### Triggers Automáticos

- ✅ `validate_estoque_carrinho` - Valida disponibilidade ao adicionar no carrinho
- ✅ `abater_estoque_pedido` - Abate estoque automaticamente ao criar pedido
- ✅ `devolver_estoque_pedido` - Devolve estoque ao cancelar pedido
- ✅ `update_timestamps` - Atualiza data de modificação automaticamente

### Dados de Exemplo

Na primeira execução, o banco é automaticamente populado com:

- 📦 **5 categorias** (Eletrônicos, Roupas, Livros, Casa, Esportes)
- 🛍️ **15 produtos** com imagens e estoque
- 👥 **2 usuários** (1 admin + 1 cliente)
- 📍 **Endereços** de exemplo
- 🖼️ **Imagens** de produtos

## 📚 Documentação

## 📚 Documentação

- 🖥️ [**Guia Tkinter**](docs/TKINTER_README.md) - Como usar a interface
- 🗄️ [**Database Initializer**](docs/DATABASE_INITIALIZER.md) - Sistema de banco de dados
- 🔑 [**Credenciais**](docs/CREDENCIAIS.md) - Usuários e dados de teste
- 📊 [**Estrutura**](docs/ESTRUTURA.md) - Organização do projeto
## 🧪 Testes

O projeto possui **112 testes automatizados** com cobertura completa do backend.

### Executar Testes

```bash
# Todos os testes
pytest

# Com relatório de cobertura
pytest --cov=src --cov-report=html

# Testes específicos
pytest tests/test_services/
pytest tests/test_repositories/
pytest tests/test_models/

# Modo verbose
pytest -v

# Parar no primeiro erro
pytest -x
```

### Estrutura de Testes

```
tests/
├── test_models/              # Testes de modelos
│   ├── test_user_model.py
│   ├── test_product_model.py
│   ├── test_cart_model.py
│   └── test_order_model.py
│
├── test_repositories/        # Testes de repositories
│   ├── test_user_repository.py
│   ├── test_product_repository.py
│   ├── test_cart_repository.py
│   └── test_order_repository.py
│
├── test_services/            # Testes de serviços
│   ├── test_auth_service.py
│   ├── test_catalog_service.py
│   ├── test_cart_service.py
│   ├── test_checkout_service.py
│   └── test_order_service.py
│
└── test_utils/               # Testes de utilitários
    ├── test_validators/
    ├── test_formatters/
    └── test_security/
```

### Cobertura de Testes

| Módulo | Cobertura | Status |
|--------|-----------|--------|
| Models | 100% | ✅ |
| Repositories | 100% | ✅ |
| Services | 100% | ✅ |
| Utils | 100% | ✅ |
| **Total Backend** | **100%** | ✅ |

### Fixtures e Mocks

Os testes utilizam fixtures pytest para:
- Mock de banco de dados
- Dados de teste consistentes
- Isolamento entre testes
- Setup/teardown automático

## ⚙️ Configuração

### Requisitos do Sistema

- **Python 3.9 ou superior**
- **Tkinter** (geralmente incluído no Python)
- **Git** (para clonar o repositório)

### Instalação do Tkinter

```bash
# Rocky Linux / RHEL / Fedora
sudo dnf install python3-tkinter

# Ubuntu / Debian
sudo apt-get install python3-tk

# macOS (via Homebrew)
brew install python-tk@3.9

# Windows
# Tkinter já vem incluído na instalação padrão do Python
```

### Instalação no Rocky Linux (XFCE)

Se estiver usando Rocky Linux com XFCE, siga o guia completo em [`docs/INSTALACAO.md`](docs/INSTALACAO.md).

**Problemas conhecidos:**
- ⚠️ Erro X11 BadLength com fontes TrueType → Ver [`docs/ERRO_X11.md`](docs/ERRO_X11.md)

### Variáveis de Ambiente (Opcional)

Crie um arquivo `.env` na raiz do projeto:

```env
# Banco de Dados
DB_PATH=database_sqlite/scee_loja.db

# Aplicação
DEBUG=True
APP_NAME=SCEE - E-commerce

# Segurança
SECRET_KEY=your-secret-key-here

# Email (futuro)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
```

### Estrutura de Diretórios Criados Automaticamente

Na primeira execução, o sistema cria:

```
database_sqlite/       # Banco de dados SQLite
  └── scee_loja.db    # Arquivo do banco

logs/                  # Logs da aplicação (futuro)
uploads/               # Imagens de produtos (futuro)
```

## 🏗️ Arquitetura

O projeto segue uma arquitetura em camadas com separation of concerns:

```
┌─────────────────────────────────────────┐
│          Views (Tkinter GUI)            │
│  LoginView, HomeView, CartView, etc.    │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│     Services (Lógica de Negócio)        │
│  AuthService, CartService, etc.         │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│   Repositories (Acesso a Dados)         │
│  UserRepository, ProductRepository      │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│         Database (SQLite)               │
│      scee_loja.db                       │
└─────────────────────────────────────────┘
```

### Design Patterns

#### Repository Pattern
Abstrai o acesso a dados, permitindo trocar a fonte sem impactar a lógica.

```python
class BaseRepository(ABC):
    @abstractmethod
    def find_by_id(self, id: int): pass
    
    @abstractmethod
    def find_all(self): pass
```

#### Service Layer
Encapsula a lógica de negócio, orquestrando repositories.

```python
class CartService:
    def __init__(self, cart_repo, product_repo):
        self.cart_repo = cart_repo
        self.product_repo = product_repo
```

#### Strategy Pattern
Permite trocar algoritmos de frete e pagamento dinamicamente.

```python
class IFreightStrategy(ABC):
    @abstractmethod
    def calculate(self, cep: str, weight: float) -> float: pass
```

### Fluxo de Dados

```
View → Service → Repository → SQLite → Repository → Service → View
```

## 📚 Documentação

- 🚀 [**Quick Start**](QUICKSTART.md) - Guia rápido de início
- 🔧 [**Instalação**](docs/INSTALACAO.md) - Instalação detalhada
- 🖥️ [**UML**](docs/UML.md) - Diagramas do sistema
- ⚠️ [**Erro X11**](docs/ERRO_X11.md) - Solução de problemas

## 🤝 Contribuindo

Contribuições são bem-vindas! Siga estes passos:

1. Fork o projeto
2. Crie sua feature branch (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'feat: adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

### Convenções de Commit (Conventional Commits)

- `feat:` - Nova funcionalidade
- `fix:` - Correção de bug
- `docs:` - Apenas documentação
- `style:` - Formatação, ponto e vírgula, etc
- `refactor:` - Refatoração de código
- `test:` - Adição/correção de testes
- `chore:` - Manutenção, dependências

### Padrões de Código

- Seguir **PEP 8** para Python
- Docstrings em todas as classes e métodos públicos
- Type hints quando possível
- Testes para novas funcionalidades

## 🐛 Reportar Bugs

Encontrou um bug? [Abra uma issue](https://github.com/daniele-senko/SCEE/issues/new) com:

- Descrição clara do problema
- Passos para reproduzir
- Comportamento esperado vs obtido
- Screenshots (se aplicável)
- Informações do sistema (OS, Python version)

## 💡 Roadmap

### Próximas Features

- [ ] 🎵 Sistema de música de fundo
- [ ] 📊 Dashboard com estatísticas em tempo real
- [ ] 🔍 Busca avançada com filtros
- [ ] ⭐ Sistema de avaliações de produtos
- [ ] 💬 Chat de suporte
- [ ] 📧 Notificações por email
- [ ] 📱 Responsividade melhorada
- [ ] 🌙 Modo escuro
- [ ] 🌍 Internacionalização (i18n)
- [ ] 📦 Rastreamento de pedidos (API Correios)

## 📄 Licença

Este é um projeto acadêmico desenvolvido para fins educacionais.

**Todos os direitos reservados © 2025**

## 👨‍💻 Autores

Desenvolvido por estudantes de Engenharia de Software:

- **Equipe SCEE** - Desenvolvimento Full Stack

## 🙏 Agradecimentos

- Professores e orientadores
- Comunidade Python Brasil
- Documentação oficial do Python e Tkinter
- Todos os contribuidores do projeto

## 📞 Contato

- **Repositório**: [github.com/daniele-senko/SCEE](https://github.com/daniele-senko/SCEE)
- **Issues**: [Reportar Problema](https://github.com/daniele-senko/SCEE/issues)
- **Pull Requests**: [Contribuir](https://github.com/daniele-senko/SCEE/pulls)

---

<div align="center">

**Desenvolvido com ❤️ para aprendizado e excelência em Engenharia de Software**

⭐ Se este projeto te ajudou, considere dar uma estrela!

*Última atualização: 29 de Novembro de 2025*

</div>
