# 🖥️ SCEE - Aplicação Desktop com Tkinter

## 📋 Sobre

SCEE (Sistema de Comércio Eletrônico) é uma aplicação desktop desenvolvida em Python com interface gráfica Tkinter e banco de dados MySQL/MariaDB.

## 🏗️ Arquitetura

### Estrutura do Projeto

```
SCEE/
├── main.py                     # Ponto de entrada da aplicação
├── gui/                        # Interface gráfica
│   ├── views/                  # Telas da aplicação
│   │   ├── login_view.py      # Tela de login
│   │   └── main_view.py       # Tela principal/dashboard
│   ├── controllers/            # Controladores
│   └── components/             # Componentes reutilizáveis
├── src/
│   ├── models/                 # Modelos de dados
│   ├── services/               # Lógica de negócio
│   │   ├── auth_service.py    # Autenticação
│   │   ├── carrinho_service.py
│   │   ├── catalogo_service.py
│   │   ├── checkout_service.py
│   │   └── pedido_service.py
│   └── integration/            # Integrações externas
├── repositories/               # Acesso a dados (MySQL)
│   ├── usuario_repository.py
│   ├── produto_repository.py
│   ├── categoria_repository.py
│   ├── carrinho_repository.py
│   └── pedido_repository.py
├── config/                     # Configurações
│   ├── database.py            # Conexão MySQL
│   └── settings.py            # Configurações gerais
├── schema/                     # Schema do banco
│   └── schema.sql
└── seed/                       # Dados iniciais
    └── seed.sql
```

## 🚀 Como Executar

### 1. Pré-requisitos

- **Python 3.9+**
- **Tkinter** (instalado no sistema)
- **MySQL/MariaDB** (via Docker ou local)

### 2. Instalar Tkinter (se necessário)

#### Rocky Linux / RHEL / Fedora:
```bash
sudo dnf install python3-tkinter
```

#### Ubuntu / Debian:
```bash
sudo apt-get install python3-tk
```

#### macOS:
```bash
# Tkinter já vem com Python instalado via Homebrew
brew install python-tk@3.9
```

### 3. Configurar Ambiente Virtual

```bash
# Criar venv
python3 -m venv .venv

# Ativar venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows
```

### 4. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 5. Iniciar MySQL/MariaDB

```bash
# Via Docker (recomendado)
docker-compose up -d

# Verificar se está rodando
docker ps | grep mariadb
```

### 6. Inicializar Banco de Dados

```bash
# Criar schema e popular dados iniciais
python init_db.py
```

### 7. Executar Aplicação

```bash
python main.py
```

## 🔐 Credenciais de Teste

Após executar `init_db.py`, você pode fazer login com:

- **Admin**: 
  - Email: `admin@scee.com`
  - Senha: `admin123`

- **Cliente**:
  - Email: `cliente@exemplo.com`
  - Senha: `cliente123`

## 🎨 Funcionalidades

### ✅ Implementadas

- [x] Tela de Login
- [x] Dashboard Principal
- [x] Navegação com Menu Lateral
- [x] Autenticação (bcrypt)
- [x] Conexão MySQL
- [x] Repositórios (7 entidades)
- [x] Services (Auth, Carrinho, Catalogo, Checkout, Pedido)

### 🚧 Em Desenvolvimento

- [ ] Tela de Produtos (listagem, busca, filtros)
- [ ] Tela de Categorias
- [ ] Tela de Carrinho de Compras
- [ ] Tela de Pedidos
- [ ] Tela de Clientes (admin)
- [ ] Tela de Administração
- [ ] Registro de novos usuários
- [ ] Perfil do usuário
- [ ] Relatórios

## 🛠️ Tecnologias

### Backend
- **Python 3.9+**
- **PyMySQL** - Driver MySQL
- **passlib/bcrypt** - Hash de senhas
- **SQLAlchemy** - ORM (opcional)

### Frontend (GUI)
- **Tkinter** - Interface gráfica nativa
- **Pillow** - Manipulação de imagens

### Banco de Dados
- **MySQL 8.0+** ou **MariaDB 12.0+**
- **Docker** - Container do banco

## 📂 Configuração

### Variáveis de Ambiente (.env)

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

### Docker Compose

```yaml
services:
  mariadb:
    image: mariadb:12
    container_name: scee_mariadb
    environment:
      MYSQL_ROOT_PASSWORD: root_password
      MYSQL_DATABASE: SCEE
      MYSQL_USER: scee_user
      MYSQL_PASSWORD: scee_pass
    ports:
      - "13306:3306"
    volumes:
      - mariadb_data:/var/lib/mysql
```

## 🧪 Testes

```bash
# Testar conexão com banco
python test_connection.py

# Testes de integração MySQL
python test_integration_mysql.py

# Testes gerais
python test_mysql.py
```

## 📝 Logs

Os logs da aplicação são salvos em:
- **Arquivo**: `scee.log`
- **Console**: stdout

## 🎯 Padrões de Código

### Repository Pattern
Cada entidade possui seu repositório para acesso a dados:

```python
from repositories.produto_repository import ProdutoRepository

repo = ProdutoRepository()
produtos = repo.listar_todos()
```

### Service Layer
Lógica de negócio centralizada nos services:

```python
from src.services.catalogo_service import CatalogoService

service = CatalogoService()
produtos = service.buscar_produtos(termo="notebook")
```

### MVC (Model-View-Controller)
- **Model**: `src/models/` - Estrutura de dados
- **View**: `gui/views/` - Interface gráfica
- **Controller**: `gui/controllers/` - Lógica da UI

## 🔧 Desenvolvimento

### Adicionar Nova Tela

1. Criar arquivo em `gui/views/nome_view.py`
2. Herdar estrutura base:

```python
class MinhaView:
    def __init__(self, parent, on_action_callback):
        self.parent = parent
        self.callback = on_action_callback
        self.create_widgets()
    
    def create_widgets(self):
        # Criar componentes Tkinter
        pass
```

3. Adicionar no menu em `main_view.py`

### Adicionar Novo Repository

1. Criar em `repositories/minha_entidade_repository.py`
2. Herdar de `BaseRepository`
3. Implementar métodos CRUD

## 📊 Banco de Dados

### Tabelas Principais

- `usuarios` - Usuários do sistema
- `clientes_info` - Informações de clientes
- `administradores` - Dados de administradores
- `enderecos` - Endereços de entrega
- `categorias` - Categorias de produtos
- `produtos` - Catálogo de produtos
- `imagens_produto` - Imagens dos produtos
- `carrinhos` - Carrinhos de compra
- `itens_carrinho` - Itens no carrinho
- `pedidos` - Pedidos realizados
- `itens_pedido` - Itens dos pedidos

### Views MySQL

- `vw_produtos_completos` - Produtos com categoria e imagens
- `vw_clientes_completos` - Clientes com dados de usuário
- `vw_pedidos_detalhados` - Pedidos com todos os dados
- `vw_carrinhos_totais` - Carrinhos com valor total

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'feat: adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto é um trabalho acadêmico.

## 👥 Autores

- DEV 1 - Backend, Database, Repositories
- DEV 2 - GUI, Frontend (Tkinter)

---

**Última atualização**: 25 de Novembro de 2025
