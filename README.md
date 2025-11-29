# 🛒 SCEE - Sistema de Comércio Eletrônico

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![SQLite](https://img.shields.io/badge/SQLite-3-orange.svg)](https://www.sqlite.org/)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)](https://docs.python.org/3/library/tkinter.html)
[![License](https://img.shields.io/badge/License-Academic-red.svg)]()

> Aplicação desktop de e-commerce desenvolvida em Python com Tkinter e SQLite

## 📋 Sobre o Projeto

SCEE é um sistema completo de comércio eletrônico desenvolvido como projeto acadêmico, implementando:

- ✅ **Interface Desktop** com Tkinter
- ✅ **Banco de Dados SQLite** (sem dependências externas)
- ✅ **Arquitetura em Camadas** (Repository Pattern, Service Layer)
- ✅ **Autenticação** com bcrypt
- ✅ **CRUD Completo** para todas as entidades

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

Na primeira execução, o banco de dados SQLite será criado automaticamente com dados iniciais!

### 🔐 Credenciais de Teste

- **Admin**: `admin@scee.com` / `admin123`
- **Cliente**: `joao@email.com` / `cliente123`

## 📁 Estrutura do Projeto

```
SCEE/
├── main.py                    # Ponto de entrada
├── init_db.py                 # Inicialização do banco
├── gui/                       # Interface Tkinter
│   ├── views/                # Telas
│   ├── controllers/          # Controladores
│   └── components/           # Componentes
├── src/
│   ├── models/               # Modelos de dados
│   ├── services/             # Lógica de negócio
│   └── utils/                # Utilitários
├── repositories/             # Acesso a dados (MySQL)
├── config/                   # Configurações
├── schema/                   # DDL MySQL
├── seed/                     # Dados iniciais
├── tests/                    # Testes
└── docs/                     # Documentação
```

📖 **Ver estrutura completa**: [`docs/ESTRUTURA.md`](docs/ESTRUTURA.md)

## 🎯 Funcionalidades

### ✅ Implementadas

- [x] Sistema de Login/Autenticação
- [x] Dashboard Principal
- [x] Gestão de Usuários
- [x] Gestão de Produtos
- [x] Gestão de Categorias
- [x] Carrinho de Compras
- [x] Sistema de Pedidos
- [x] Endereços de Entrega

### 🚧 Em Desenvolvimento

- [ ] Interface de Produtos (GUI)
- [ ] Interface de Categorias (GUI)
- [ ] Interface de Carrinho (GUI)
- [ ] Interface de Pedidos (GUI)
- [ ] Relatórios e Dashboard
- [ ] Sistema de Pagamento

## 🛠️ Tecnologias

### Backend
- **Python 3.9+**
- **SQLite3** - Banco de dados embutido
- **bcrypt/passlib** - Criptografia de senhas

### Frontend
- **Tkinter** - Interface gráfica nativa
- **Pillow** - Processamento de imagens

### Banco de Dados
- **SQLite 3** - Banco de dados local (sem instalação adicional)

## 📚 Documentação

## 📚 Documentação

- 🖥️ [**Guia Tkinter**](docs/TKINTER_README.md) - Como usar a interface
- 🗄️ [**Database Initializer**](docs/DATABASE_INITIALIZER.md) - Sistema de banco de dados
- 🔑 [**Credenciais**](docs/CREDENCIAIS.md) - Usuários e dados de teste
- 📊 [**Estrutura**](docs/ESTRUTURA.md) - Organização do projeto
## 🧪 Testes

```bash
# Executar todos os testes
pytest tests/

# Testes específicos
pytest tests/test_database.py
```

## ⚙️ Configuração

### Requisitos do Sistema

- **Python 3.9+**
### Requisitos do Sistema

- **Python 3.9+**
- **Tkinter** (geralmente incluído no Python)
- **Git**
```bash
# Rocky Linux / RHEL / Fedora
sudo dnf install python3-tkinter

# Ubuntu / Debian
sudo apt-get install python3-tk

# macOS (via Homebrew)
brew install python-tk@3.9
```

### Variáveis de Ambiente

Copiar `.env.example` para `.env` e ajustar:

### Variáveis de Ambiente

Copiar `.env.example` para `.env` e ajustar se necessário:

```env
# Banco de Dados (SQLite)
DB_NAME=scee_loja.db

# Aplicação
DEBUG=True
SECRET_KEY=seu-secret-key-aqui
``` Schema

O banco possui 11 tabelas principais:
## 🗄️ Banco de Dados

### SQLite - Banco Embutido

O projeto utiliza SQLite, um banco de dados leve e sem necessidade de servidor. O arquivo do banco é criado automaticamente em `database_sqlite/scee_loja.db`.

### Schema

O banco possui 11 tabelas principais:
- `usuarios`, `clientes_info`, `administradores`
- `enderecos`, `categorias`, `produtos`, `imagens_produto`
- `carrinhos`, `itens_carrinho`, `pedidos`, `itens_pedido`

### Views

- `vw_produtos_completos` - Produtos com categoria e imagens
- `vw_clientes_completos` - Clientes com dados completos
- `vw_pedidos_detalhados` - Pedidos com todos os detalhes
- `vw_carrinhos_totais` - Carrinhos com valor total

### Triggers

- `validate_estoque_carrinho` - Valida estoque ao adicionar no carrinho
- `abater_estoque_pedido` - Abate estoque ao criar pedido
- `devolver_estoque_pedido` - Devolve estoque ao cancelar pedido
- Triggers de atualização automática de timestamps

### Dados Iniciais

Na primeira execução, o banco é populado automaticamente com:
- 5 categorias de produtos
- 15 produtos com estoque
- 2 usuários (1 admin + 1 cliente)
- Endereços e imagens de exemplo
- **Repository Pattern** - Abstração de acesso a dados
- **Service Layer** - Lógica de negócio centralizada
- **MVC** - Model-View-Controller para GUI

### Fluxo de Dados

```
### Fluxo de Dados

```
GUI (Views) → Controllers → Services → Repositories → SQLite
```
1. Fork o projeto
2. Crie sua feature branch (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'feat: adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

### Convenções de Commit

- `feat:` - Nova funcionalidade
- `fix:` - Correção de bug
- `docs:` - Documentação
- `chore:` - Manutenção
- `refactor:` - Refatoração
- `test:` - Testes

## 📄 Licença

Projeto acadêmico - Todos os direitos reservados.

## 👨‍💻 Autores

- **DEV 1** - Backend, Database, Repositories
- **DEV 2** - Frontend, GUI (Tkinter)

## 📞 Contato

- **Repositório**: [github.com/daniele-senko/SCEE](https://github.com/daniele-senko/SCEE)
- **Issues**: [github.com/daniele-senko/SCEE/issues](https://github.com/daniele-senko/SCEE/issues)
---

**Desenvolvido com ❤️ por estudantes para estudantes**

*Última atualização: 29 de Novembro de 2025*
*Última atualização: 25 de Novembro de 2025*
