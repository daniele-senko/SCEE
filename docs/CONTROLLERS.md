# 🎮 Controllers - Camada de Controle SCEE

## 📋 Visão Geral

A camada de **Controllers** implementa o padrão **MVC (Model-View-Controller)**, separando as responsabilidades:

- **View**: Interface gráfica (Tkinter) - apenas renderização
- **Controller**: Orquestração e lógica de fluxo - **ESTA CAMADA**
- **Service**: Regras de negócio
- **Repository**: Persistência de dados

## 🏗️ Arquitetura

```
┌──────────────┐
│     View     │ (Tkinter - UI)
│  login_view  │
└──────┬───────┘
       │ evento (clique botão)
       ↓
┌──────────────┐
│  Controller  │ (Orquestração)
│AuthController│
└──────┬───────┘
       │ chama
       ↓
┌──────────────┐
│   Service    │ (Regras de negócio)
│ AuthService  │
└──────┬───────┘
       │ chama
       ↓
┌──────────────┐
│  Repository  │ (Persistência)
│UsuarioRepo   │
└──────┬───────┘
       │ SQL
       ↓
┌──────────────┐
│   Database   │ (SQLite)
│  usuarios    │
└──────────────┘
```

## 📁 Estrutura de Arquivos

```
src/controllers/
├── __init__.py              # Exports
├── base_controller.py       # Classe base abstrata
├── auth_controller.py       # Autenticação
├── catalog_controller.py    # Catálogo
├── cart_controller.py       # Carrinho
├── order_controller.py      # Pedidos
└── admin_controller.py      # Administração
```

## 🎯 Controllers Implementados

### 1️⃣ BaseController (Abstrato)

**Arquivo:** `base_controller.py`

**Responsabilidades:**
- Define contrato para todos os controllers
- Métodos utilitários comuns
- Padronização de respostas

**Métodos Principais:**
```python
_success_response(message, data=None)  # Resposta de sucesso
_error_response(message, error=None)   # Resposta de erro
_validate_not_empty(value, field)      # Validação básica
_validate_min_length(value, field, min_length)
navigate_to(view_name, data=None)      # Navegação entre views
```

**Formato de Resposta Padronizado:**
```python
{
    'success': True/False,
    'message': 'Mensagem amigável',
    'data': {...},  # Dados opcionais
    'error': 'Erro técnico'  # Apenas em erros
}
```

---

### 2️⃣ AuthController

**Arquivo:** `auth_controller.py`

**Responsabilidades:**
- Login de usuários
- Registro de novos clientes
- Logout
- Validação de credenciais

**Métodos:**

#### `login(email: str, senha: str) -> Dict`
Autentica usuário e navega para tela apropriada.

**Validações:**
- ✅ Email não vazio
- ✅ Senha não vazia
- ✅ Formato de email válido

**Fluxo:**
```python
1. Validar inputs
2. Chamar AuthService.login()
3. Se sucesso:
   - Admin → AdminDashboard
   - Cliente → HomeView
4. Retornar resultado
```

**Exemplo de Uso:**
```python
from src.controllers.auth_controller import AuthController

controller = AuthController(main_window)
result = controller.login("joao@email.com", "senha123")

if result['success']:
    print(result['message'])  # "Bem-vindo, João!"
else:
    print(result['message'])  # "Email ou senha incorretos"
```

#### `register_client(...) -> Dict`
Registra novo cliente.

**Parâmetros:**
- `nome`: Nome completo
- `email`: Email único
- `cpf`: CPF (11 dígitos)
- `senha`: Senha (mínimo 6 caracteres)
- `confirmar_senha`: Confirmação

**Validações:**
- ✅ Todos os campos preenchidos
- ✅ Nome com mínimo 3 caracteres
- ✅ Email válido
- ✅ CPF válido (11 dígitos, não repetido)
- ✅ Senha mínimo 6 caracteres
- ✅ Senhas coincidem
- ✅ Email não cadastrado

#### `logout() -> Dict`
Desconecta usuário e retorna ao login.

---

### 3️⃣ CatalogController

**Arquivo:** `catalog_controller.py`

**Responsabilidades:**
- Listagem de produtos
- Busca e filtros
- Navegação de catálogo

**Métodos:**

#### `list_products(categoria_id=None) -> Dict`
Lista produtos, opcionalmente filtrados por categoria.

**Retorna:** Lista de produtos ativos

#### `list_categories() -> Dict`
Lista todas as categorias.

#### `get_product_details(produto_id: int) -> Dict`
Obtém detalhes de um produto específico.

#### `search_products(termo: str) -> Dict`
Busca produtos por nome ou descrição.

**Exemplo:**
```python
controller = CatalogController(main_window)

# Listar todos os produtos
result = controller.list_products()
produtos = result['data']  # Lista de Produto

# Filtrar por categoria
result = controller.list_products(categoria_id=1)

# Buscar
result = controller.search_products("notebook")
```

#### `view_product_details(produto_id: int) -> Dict`
Navega para tela de detalhes do produto.

---

### 4️⃣ CartController

**Arquivo:** `cart_controller.py`

**Responsabilidades:**
- Adicionar/remover produtos do carrinho
- Atualizar quantidades
- Calcular totais
- Iniciar checkout

**Métodos:**

#### `set_current_user(usuario_id: int)`
Define o usuário logado (obrigatório).

#### `add_to_cart(produto_id: int, quantidade: int) -> Dict`
Adiciona produto ao carrinho.

**Validações:**
- ✅ Usuário autenticado
- ✅ Quantidade > 0
- ✅ Produto existe
- ✅ Estoque disponível
- ✅ Limites do carrinho

**Exemplo:**
```python
controller = CartController(main_window)
controller.set_current_user(usuario_id=1)

result = controller.add_to_cart(produto_id=5, quantidade=2)

if result['success']:
    print("Produto adicionado!")
else:
    print(result['message'])  # "Produto sem estoque disponível"
```

#### `remove_from_cart(item_id: int) -> Dict`
Remove item do carrinho.

#### `update_quantity(item_id: int, nova_quantidade: int) -> Dict`
Atualiza quantidade de item.
- Se `nova_quantidade == 0`, remove item
- Valida estoque disponível

#### `get_cart() -> Dict`
Obtém carrinho com itens e total.

**Retorna:**
```python
{
    'carrinho': {...},
    'itens': [...],
    'total': 150.00,
    'quantidade_itens': 3
}
```

#### `clear_cart() -> Dict`
Limpa todo o carrinho.

#### `proceed_to_checkout() -> Dict`
Valida carrinho e navega para checkout.

---

### 5️⃣ OrderController

**Arquivo:** `order_controller.py`

**Responsabilidades:**
- Criar pedidos
- Listar pedidos do usuário
- Cancelar pedidos
- Visualizar detalhes

**Métodos:**

#### `create_order(...) -> Dict`
Cria novo pedido.

**Parâmetros:**
- `endereco_id`: Endereço de entrega
- `itens`: Lista de `{produto_id, quantidade, preco_unitario}`
- `tipo_pagamento`: "PIX", "CARTAO" ou "BOLETO"
- `frete`: Valor do frete
- `observacoes`: Opcional

**Validações:**
- ✅ Usuário autenticado
- ✅ Pelo menos um item
- ✅ Tipo de pagamento válido
- ✅ Estoque disponível

**Exemplo:**
```python
controller = OrderController(main_window)
controller.set_current_user(usuario_id=1)

result = controller.create_order(
    endereco_id=2,
    itens=[
        {'produto_id': 5, 'quantidade': 2, 'preco_unitario': 50.00},
        {'produto_id': 7, 'quantidade': 1, 'preco_unitario': 100.00}
    ],
    tipo_pagamento='PIX',
    frete=15.00
)

if result['success']:
    print(result['message'])  # "Pedido #123 criado com sucesso!"
```

#### `get_my_orders(status=None, limit=10) -> Dict`
Lista pedidos do usuário.

**Retorna:** Lista de pedidos

#### `get_order_details(pedido_id: int) -> Dict`
Detalhes completos do pedido com itens.

**Validações:**
- ✅ Pedido existe
- ✅ Pedido pertence ao usuário

#### `cancel_order(pedido_id: int) -> Dict`
Cancela pedido.

**Validações:**
- ✅ Pedido pertence ao usuário
- ✅ Status permite cancelamento
- ✅ Dentro do prazo (24h)

---

### 6️⃣ AdminController

**Arquivo:** `admin_controller.py`

**Responsabilidades:**
- CRUD de produtos
- Gestão de pedidos
- Estatísticas do dashboard

**Métodos:**

#### `create_product(...) -> Dict`
Cria novo produto.

**Parâmetros:**
- `nome`: Nome do produto
- `sku`: SKU único
- `preco`: Preço (> 0)
- `estoque`: Quantidade (>= 0)
- `categoria_nome`: Nome da categoria
- `descricao`: Descrição (opcional)

**Validações:**
- ✅ Admin autenticado
- ✅ Campos obrigatórios preenchidos
- ✅ Preço > 0
- ✅ Estoque >= 0
- ✅ SKU único

#### `update_product(produto_id, ...) -> Dict`
Atualiza produto existente.

**Permite atualizar:**
- Nome, preço, estoque, descrição, status ativo

#### `delete_product(produto_id: int) -> Dict`
Remove produto.

#### `list_all_orders(status=None, limit=50) -> Dict`
Lista todos os pedidos (visão admin).

#### `update_order_status(pedido_id, novo_status) -> Dict`
Atualiza status do pedido.

**Status válidos:**
- PENDENTE → PROCESSANDO
- PROCESSANDO → ENVIADO
- ENVIADO → ENTREGUE
- Qualquer → CANCELADO

**Validações:**
- ✅ Transição de status permitida

#### `get_dashboard_stats() -> Dict`
Estatísticas para o dashboard admin.

**Retorna:**
```python
{
    'total_produtos': 50,
    'total_categorias': 10,
    'pedidos_pendentes': 5,
    'pedidos_processando': 3,
    'pedidos_enviados': 2,
    'total_vendas': 5000.00
}
```

**Exemplo:**
```python
controller = AdminController(main_window)
controller.set_current_admin(admin_id=1)

# Dashboard
result = controller.get_dashboard_stats()
stats = result['data']
print(f"Vendas: R$ {stats['total_vendas']:.2f}")

# Criar produto
result = controller.create_product(
    nome="Notebook Dell",
    sku="NB-DELL-001",
    preco=2500.00,
    estoque=10,
    categoria_nome="Eletrônicos"
)
```

---

## 🔄 Fluxo de Dados Completo

### Exemplo: Login de Usuário

```
┌─────────────────────────────────────────────────┐
│ 1. VIEW (login_view.py)                        │
│    - Usuário clica em "ENTRAR"                 │
│    - Captura email e senha dos inputs          │
│    - Chama controller.login(email, senha)      │
└─────────────────┬───────────────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────────────┐
│ 2. CONTROLLER (auth_controller.py)             │
│    - Valida email não vazio                    │
│    - Valida senha não vazia                    │
│    - Valida formato de email                   │
│    - Chama auth_service.login(email, senha)    │
└─────────────────┬───────────────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────────────┐
│ 3. SERVICE (auth_service.py)                   │
│    - Busca usuário no repository               │
│    - Verifica senha com PasswordHasher         │
│    - Armazena usuário logado                   │
│    - Retorna True/False                        │
└─────────────────┬───────────────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────────────┐
│ 4. REPOSITORY (user_repository.py)             │
│    - Executa query SQL                         │
│    - Retorna objeto Usuario                    │
└─────────────────┬───────────────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────────────┐
│ 5. CONTROLLER (decisão de navegação)           │
│    - Se Admin: main_window.show_view('Admin')  │
│    - Se Cliente: main_window.show_view('Home') │
│    - Retorna resultado para View               │
└─────────────────┬───────────────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────────────┐
│ 6. VIEW (resposta)                             │
│    - if result['success']:                     │
│        messagebox.showinfo(result['message'])  │
│    - else:                                     │
│        messagebox.showerror(result['message']) │
└─────────────────────────────────────────────────┘
```

---

## ✅ Benefícios da Arquitetura com Controllers

### 1️⃣ **Separação de Responsabilidades**
```
View:       "O QUE mostrar"     → Apenas UI
Controller: "COMO orquestrar"   → Fluxo e validações
Service:    "REGRAS DE NEGÓCIO" → Lógica complexa
Repository: "ONDE salvar"       → Persistência
```

### 2️⃣ **Testabilidade**
```python
# Testar controller SEM precisar de UI
def test_login_sucesso():
    controller = AuthController(mock_main_window)
    result = controller.login("admin@scee.com", "admin123")
    
    assert result['success'] == True
    assert "Bem-vindo" in result['message']
```

### 3️⃣ **Reusabilidade**
```python
# Mesmo controller funciona para:
- Interface Desktop (Tkinter)
- Interface Web (Flask/Django)
- API REST (FastAPI)
- CLI (terminal)
```

### 4️⃣ **Manutenibilidade**
```
Mudança na UI:     Editar apenas Views
Mudança no fluxo:  Editar apenas Controllers
Mudança em regras: Editar apenas Services
Mudança em dados:  Editar apenas Repositories
```

---

## 📖 Como Usar os Controllers

### Padrão nas Views

**ANTES (sem controller):**
```python
# ❌ View fazendo TUDO
class LoginView(tk.Frame):
    def __init__(self, parent, controller):
        self.auth_service = AuthService()  # ❌ View conhece Service
    
    def _handle_login(self):
        email = self.entry_email.get()
        senha = self.entry_senha.get()
        
        # ❌ Validações na View
        if not email:
            messagebox.showerror("Erro", "Email vazio")
            return
        
        # ❌ Chamada direta ao Service
        if self.auth_service.login(email, senha):
            # ❌ Decisão de navegação na View
            usuario = self.auth_service.get_usuario_atual()
            if usuario.tipo == 'admin':
                self.controller.show_view('AdminDashboard')
```

**DEPOIS (com controller):**
```python
# ✅ View APENAS renderiza e captura eventos
class LoginView(tk.Frame):
    def __init__(self, parent, main_window):
        # View não conhece Services!
        pass
    
    def _handle_login(self):
        # 1. Capturar dados
        email = self.entry_email.get()
        senha = self.entry_senha.get()
        
        # 2. Delegar para Controller
        from src.controllers.auth_controller import AuthController
        controller = AuthController(self.controller)
        result = controller.login(email, senha)
        
        # 3. Exibir resultado
        if result['success']:
            messagebox.showinfo('Sucesso', result['message'])
        else:
            messagebox.showerror('Erro', result['message'])
```

---

## 🧪 Testando Controllers

```python
# tests/test_auth_controller.py
import pytest
from src.controllers.auth_controller import AuthController
from unittest.mock import Mock

def test_login_email_vazio():
    """Controller deve validar email vazio."""
    mock_window = Mock()
    controller = AuthController(mock_window)
    
    result = controller.login("", "senha123")
    
    assert result['success'] == False
    assert "Email" in result['message']

def test_login_sucesso():
    """Login válido deve navegar para HomeView."""
    mock_window = Mock()
    controller = AuthController(mock_window)
    
    result = controller.login("joao@email.com", "cliente123")
    
    assert result['success'] == True
    mock_window.show_view.assert_called_once_with('HomeView', ...)
```

---

## 🔗 Próximos Passos

1. ✅ **Controllers criados**
2. ⏭️ **Refatorar Views** para usar controllers
3. ⏭️ **Criar testes** para todos os controllers
4. ⏭️ **Atualizar UML** com camada de controllers

---

**Desenvolvido com 💙 seguindo padrão MVC**
