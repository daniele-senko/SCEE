# DEV 1 - Banco de Dados e Repositórios

## ✅ Trabalho Concluído

### 1. Schema Completo SQLite
- ✅ 11 tabelas criadas (`schema/schema.sql`)
- ✅ Índices para performance
- ✅ Foreign keys e constraints
- ✅ Triggers para validação e timestamps automáticos

### 2. Repositórios Implementados
- ✅ `BaseRepository` - Interface abstrata
- ✅ `UsuarioRepository` - Gerenciamento de usuários
- ✅ `ClienteRepository` - Informações de clientes
- ✅ `EnderecoRepository` - Endereços dos clientes
- ✅ `CategoriaRepository` - Categorias de produtos
- ✅ `ProdutoRepository` - Produtos com busca avançada
- ✅ `CarrinhoRepository` - Carrinho de compras
- ✅ `PedidoRepository` - Pedidos e itens

### 3. Configurações
- ✅ `config/database.py` - Conexão SQLite
- ✅ `config/settings.py` - Configurações com Pydantic
- ✅ `seed/seed.sql` - Dados iniciais
- ✅ `requirements.txt` - Dependências

## 🚀 Como Usar

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Inicializar Banco de Dados

**Criar apenas o schema:**
```bash
python init_db.py
```

**Criar schema + dados de exemplo:**
```bash
python init_db.py --seed
```

**Resetar banco (apaga tudo e recria):**
```bash
python init_db.py --reset --seed
```

### 3. Testar Repositórios

```python
from config.database import get_connection
from repositories.usuario_repository import UsuarioRepository

# Criar repositório
repo = UsuarioRepository(get_connection)

# Listar usuários
usuarios = repo.listar()
print(f"Total de usuários: {len(usuarios)}")

# Buscar por email
admin = repo.buscar_por_email('admin@scee.com')
print(f"Admin: {admin['nome']}")
```

## 📊 Estrutura do Banco

### Tabelas Principais
1. `usuarios` - Usuários base (clientes e admins)
2. `clientes_info` - Dados específicos de clientes (CPF, telefone)
3. `administradores` - Dados específicos de admins
4. `enderecos` - Endereços dos usuários
5. `categorias` - Categorias de produtos
6. `produtos` - Catálogo de produtos
7. `imagens_produto` - Imagens dos produtos
8. `carrinhos` - Carrinhos de compra
9. `itens_carrinho` - Itens nos carrinhos
10. `pedidos` - Pedidos realizados
11. `itens_pedido` - Itens dos pedidos

### Dados de Seed Incluídos
- **Categorias:** 5 categorias (Eletrônicos, Roupas, Livros, Casa, Esportes)
- **Produtos:** 15 produtos de exemplo
- **Usuários:**
  - Admin: `admin@scee.com` / `admin123`
  - Cliente: `joao@email.com` / `cliente123`

## 🔧 Próximos Passos (DEV 1)

### Semana 2 (12-17/11)
- [ ] Implementar API REST com FastAPI
- [ ] Criar rotas de autenticação (login/register)
- [ ] Criar middleware de autenticação JWT
- [ ] Implementar rotas de produtos
- [ ] Testar com Postman

### Arquivos a Criar
```
api/
├── main.py                    # Setup FastAPI
├── middlewares/
│   └── auth_middleware.py     # Verificar JWT
├── schemas/
│   ├── usuario_schema.py      # DTOs de validação
│   └── produto_schema.py
└── routes/
    ├── auth_routes.py         # POST /login, /register
    └── produto_routes.py      # GET /produtos
```

## 📝 Comandos Git Úteis

### Ver branches criadas
```bash
git branch
```

### Mesclar branches (depois de revisar)
```bash
git checkout main
git merge feature/SCEE-2.1.1-schema-usuarios
git merge feature/SCEE-2.4.1-base-repository
git merge feature/SCEE-4.1.1-carrinho-pedido-repositories
```

### Fazer push para o GitHub
```bash
git push origin feature/SCEE-2.1.1-schema-usuarios
git push origin feature/SCEE-2.4.1-base-repository
git push origin feature/SCEE-4.1.1-carrinho-pedido-repositories
```

## 🎯 Padrões Seguidos

- **Repository Pattern:** Abstração completa de acesso a dados
- **Type Hints:** Todos os métodos documentados com tipos
- **Docstrings:** Documentação completa em português
- **CRUD Completo:** Todos os repositórios implementam interface base
- **Métodos Específicos:** Cada repositório tem métodos próprios conforme necessidade
- **Transações:** Uso de context managers para garantir commits
