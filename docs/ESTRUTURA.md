# 📁 Estrutura do Projeto SCEE

## 🗂️ Organização de Diretórios

```
SCEE/
├── 📄 main.py                    # Ponto de entrada da aplicação
├── 📄 init_db.py                 # Script de inicialização do banco
├── 📄 requirements.txt           # Dependências Python
├── 📄 compose.yaml               # Docker Compose (MariaDB)
├── 📄 .env.example               # Exemplo de variáveis de ambiente
├── 📄 README.md                  # Documentação principal
│
├── 📁 gui/                       # Interface Gráfica (Tkinter)
│   ├── views/                    # Telas da aplicação
│   │   ├── login_view.py        # Tela de login
│   │   └── main_view.py         # Dashboard principal
│   ├── controllers/              # Controladores (lógica UI)
│   └── components/               # Componentes reutilizáveis
│
├── 📁 src/                       # Código-fonte principal
│   ├── models/                   # Modelos de dados
│   │   ├── users/               # Modelos de usuários
│   │   ├── products/            # Modelos de produtos
│   │   ├── pedido.py
│   │   ├── item_pedido.py
│   │   ├── endereco.py
│   │   └── enums.py
│   │
│   ├── services/                 # Lógica de negócio
│   │   ├── auth_service.py      # Autenticação
│   │   ├── catalogo_service.py  # Catálogo de produtos
│   │   ├── carrinho_service.py  # Carrinho de compras
│   │   ├── checkout_service.py  # Finalização de pedido
│   │   ├── pedido_service.py    # Gestão de pedidos
│   │   ├── usuario_service.py   # Gestão de usuários
│   │   └── email_service.py     # Envio de emails
│   │
│   ├── utils/                    # Utilitários
│   │   ├── validators/          # Validadores
│   │   ├── formatters.py        # Formatação
│   │   └── security/            # Segurança
│   │
│   ├── integration/              # Integrações externas
│   │   └── pagamento_gateway.py
│   │
│   ├── interfaces/               # Interfaces/Contratos
│   │   └── i_repository.py
│   │
│   └── config/                   # Configurações (duplicata)
│       ├── database.py
│       └── settings.py
│
├── 📁 repositories/              # Acesso a Dados (MySQL)
│   ├── base_repository.py       # Repository base
│   ├── usuario_repository.py    # Usuários
│   ├── cliente_repository.py    # Clientes
│   ├── endereco_repository.py   # Endereços
│   ├── categoria_repository.py  # Categorias
│   ├── produto_repository.py    # Produtos
│   ├── carrinho_repository.py   # Carrinhos
│   └── pedido_repository.py     # Pedidos
│
├── 📁 config/                    # Configurações principais
│   ├── database.py              # Conexão MySQL
│   └── settings.py              # Settings da aplicação
│
├── 📁 schema/                    # Schema do Banco de Dados
│   └── schema.sql               # DDL MySQL
│
├── 📁 seed/                      # Dados Iniciais
│   └── seed.sql                 # Dados de seed
│
├── 📁 tests/                     # Testes
│   ├── test_connection.py       # Teste de conexão
│   ├── test_mysql.py            # Testes MySQL
│   └── test_integration_mysql.py # Testes de integração
│
├── 📁 docs/                      # Documentação
│   ├── TKINTER_README.md        # Guia Tkinter
│   ├── MYSQL_README.md          # Guia MySQL
│   ├── DEV1_README.md           # README Dev 1
│   ├── VERIFICACAO_MYSQL.md     # Relatório MySQL
│   ├── UML.md                   # Diagramas UML
│   ├── Classe_UML.webp          # Diagrama de classes
│   └── ESTRUTURA.md             # Este arquivo
│
└── 📁 manuais/                   # Manuais diversos
    └── Usando env.md
```

## 🎯 Camadas da Aplicação

### 1. **Apresentação (GUI)**
- **Localização**: `gui/`
- **Responsabilidade**: Interface gráfica com Tkinter
- **Componentes**: Views, Controllers, Components

### 2. **Lógica de Negócio (Services)**
- **Localização**: `src/services/`
- **Responsabilidade**: Regras de negócio e orquestração
- **Componentes**: Auth, Catálogo, Carrinho, Checkout, Pedidos

### 3. **Acesso a Dados (Repositories)**
- **Localização**: `repositories/`
- **Responsabilidade**: CRUD e queries MySQL
- **Padrão**: Repository Pattern

### 4. **Modelos (Models)**
- **Localização**: `src/models/`
- **Responsabilidade**: Estruturas de dados
- **Tipos**: Users, Products, Orders

### 5. **Configuração**
- **Localização**: `config/`
- **Responsabilidade**: Settings e conexões
- **Arquivos**: database.py, settings.py

## 📝 Convenções

### Nomenclatura
- **Arquivos**: `snake_case.py`
- **Classes**: `PascalCase`
- **Funções**: `snake_case()`
- **Constantes**: `UPPER_SNAKE_CASE`

### Estrutura de Arquivos
- Cada repository em arquivo próprio
- Cada service em arquivo próprio
- Views agrupadas por funcionalidade
- Models organizados por domínio

## 🔧 Arquivos de Configuração

- **`.env`**: Variáveis de ambiente (não versionado)
- **`.env.example`**: Template de variáveis
- **`compose.yaml`**: Docker Compose
- **`requirements.txt`**: Dependências Python
- **`.gitignore`**: Arquivos ignorados pelo Git

## 📊 Banco de Dados

### Schema
- **Localização**: `schema/schema.sql`
- **Tipo**: MySQL 8.0+ / MariaDB 12.0+
- **Tabelas**: 11 tabelas principais
- **Views**: 4 views de consulta

### Seed
- **Localização**: `seed/seed.sql`
- **Conteúdo**: Dados iniciais de teste
- **Executar**: Via `init_db.py`

## 🧪 Testes

### Estrutura
- **Unit Tests**: Testes de unidade
- **Integration Tests**: Testes de integração MySQL
- **Connection Tests**: Testes de conexão

### Executar
```bash
# Todos os testes
pytest tests/

# Teste específico
python tests/test_integration_mysql.py
```

## 📚 Documentação

Toda documentação está em `docs/`:
- **TKINTER_README.md**: Guia completo da GUI
- **MYSQL_README.md**: Documentação do banco
- **VERIFICACAO_MYSQL.md**: Relatório de migração
- **UML.md**: Diagramas e modelagem

---

**Última atualização**: 25 de Novembro de 2025
