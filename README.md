# 🛒 SCEE - Sistema de Comércio Eletrônico

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)](https://www.mysql.com/)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)](https://docs.python.org/3/library/tkinter.html)
[![License](https://img.shields.io/badge/License-Academic-red.svg)]()

> Aplicação desktop de e-commerce desenvolvida em Python com Tkinter e MySQL/MariaDB

## 📋 Sobre o Projeto

SCEE é um sistema completo de comércio eletrônico desenvolvido como projeto acadêmico, implementando:

- ✅ **Interface Desktop** com Tkinter
- ✅ **Banco de Dados MySQL/MariaDB** via Docker
- ✅ **Arquitetura em Camadas** (Repository Pattern, Service Layer)
- ✅ **Autenticação** com bcrypt
- ✅ **CRUD Completo** para todas as entidades

## 🚀 Quick Start

### Método 1: Script Automático (Recomendado)

```bash
# Linux / macOS
./run.sh

# Windows
run.bat
```

O script automático faz tudo: cria venv, instala dependências, inicia Docker e executa a aplicação!

### Método 2: Manual

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

# 4. Iniciar banco de dados (Docker)
docker compose up -d

# 5. Aguardar e verificar banco (~30s)
python init_db.py --wait

# 6. Executar aplicação
python main.py
```

### 🔐 Credenciais de Teste

- **Admin**: `admin@scee.com` / `admin123`
- **Cliente**: `cliente@exemplo.com` / `cliente123`

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
- **PyMySQL** - Driver MySQL
- **bcrypt/passlib** - Criptografia de senhas
- **SQLAlchemy** - ORM

### Frontend
- **Tkinter** - Interface gráfica nativa
- **Pillow** - Processamento de imagens

### Banco de Dados
- **MySQL 8.0+** / **MariaDB 12.0+**
- **Docker** para containerização

## 📚 Documentação

- 🖥️ [**Guia Tkinter**](docs/TKINTER_README.md) - Como usar a interface
- 🗄️ [**Guia MySQL**](docs/MYSQL_README.md) - Documentação do banco
- 📊 [**Estrutura**](docs/ESTRUTURA.md) - Organização do projeto
- ✅ [**Verificação MySQL**](docs/VERIFICACAO_MYSQL.md) - Relatório de migração
- 📐 [**UML**](docs/UML.md) - Diagramas e modelagem

## 🧪 Testes

```bash
# Teste de conexão
python tests/test_connection.py

# Testes de integração MySQL
python tests/test_integration_mysql.py

# Todos os testes
pytest tests/
```

## ⚙️ Configuração

### Requisitos do Sistema

- **Python 3.9+**
- **Tkinter** (geralmente incluído no Python)
- **Docker** e **Docker Compose**
- **Git**

### Instalar Tkinter (se necessário)

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

```env
# MySQL
MYSQL_HOST=localhost
MYSQL_PORT=13306
MYSQL_USER=scee_user
MYSQL_PASSWORD=scee_pass
MYSQL_DATABASE=SCEE

# Aplicação
DEBUG=True
SECRET_KEY=seu-secret-key-aqui
```

## 🗄️ Banco de Dados

### Schema

O banco possui 11 tabelas principais:
- `usuarios`, `clientes_info`, `administradores`
- `enderecos`, `categorias`, `produtos`, `imagens_produto`
- `carrinhos`, `itens_carrinho`, `pedidos`, `itens_pedido`

### Views MySQL

- `vw_produtos_completos` - Produtos com categoria e imagens
- `vw_clientes_completos` - Clientes com dados completos
- `vw_pedidos_detalhados` - Pedidos com todos os detalhes
- `vw_carrinhos_totais` - Carrinhos com valor total

### Docker

O banco roda em container MariaDB:

```bash
# Iniciar
docker-compose up -d

# Parar
docker-compose down

# Ver logs
docker-compose logs -f mariadb

# Acessar MySQL CLI
docker exec -it scee_mariadb mysql -uscee_user -pscee_pass SCEE
```

## 🏗️ Arquitetura

### Padrões Utilizados

- **Repository Pattern** - Abstração de acesso a dados
- **Service Layer** - Lógica de negócio centralizada
- **MVC** - Model-View-Controller para GUI

### Fluxo de Dados

```
GUI (Views) → Controllers → Services → Repositories → MySQL
```

## 👥 Contribuindo

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

*Última atualização: 25 de Novembro de 2025*
