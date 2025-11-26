# Services Implementados - SCEE

Documentação completa dos serviços implementados com validações básicas e avançadas.

## 📋 Sumário

- [CarrinhoService](#carrinhoservice) - `feature/SCEE-5.1-carrinho-service`
- [PedidoService](#pedidoservice) - `feature/SCEE-5.2-pedido-service`
- [CatalogoService](#catalogoservice) - `feature/SCEE-5.3-catalogo-service`
- [UsuarioService](#usuarioservice) - `feature/SCEE-5.4-usuario-service`
- [EmailService](#emailservice) - `feature/SCEE-5.5-email-service`

---

## 🛒 CarrinhoService

**Branch:** `feature/SCEE-5.1-carrinho-service`

### Funcionalidades

- ✅ Adicionar itens ao carrinho
- ✅ Remover itens do carrinho
- ✅ Atualizar quantidade de itens
- ✅ Listar itens do carrinho
- ✅ Calcular total do carrinho
- ✅ Limpar carrinho
- ✅ Validar carrinho para checkout

### Validações Básicas

- Quantidade mínima: 1
- Quantidade máxima por item: 100
- ID de usuário válido

### Validações Avançadas

- **Estoque:** Verifica disponibilidade antes de adicionar
- **Limites:**
  - Máximo 50 itens no carrinho
  - Valor máximo: R$ 50.000,00
- **Produto:** Valida se está ativo e disponível
- **Preços:** Valida alterações de preço durante checkout
- **Integridade:** Considera itens já no carrinho ao validar estoque

### Exceções

- `CarrinhoServiceError` - Erro genérico
- `ProdutoIndisponivelError` - Produto não disponível
- `EstoqueInsuficienteError` - Estoque insuficiente
- `LimiteCarrinhoExcedidoError` - Limite excedido
- `PrecoInvalidoError` - Preço inválido

### Exemplo de Uso

```python
from repositories.carrinho_repository import CarrinhoRepository
from repositories.produto_repository import ProdutoRepository
from src.services.carrinho_service import CarrinhoService
from config.database import get_connection

carrinho_repo = CarrinhoRepository(get_connection)
produto_repo = ProdutoRepository(get_connection)
service = CarrinhoService(carrinho_repo, produto_repo)

# Adicionar item
item = service.adicionar_item(
    usuario_id=1,
    produto_id=10,
    quantidade=2
)

# Validar para checkout
validacao = service.validar_carrinho_para_compra(usuario_id=1)
if validacao['valido']:
    print(f"Carrinho válido! Total: R$ {validacao['valor_total']:.2f}")
```

---

## 📦 PedidoService

**Branch:** `feature/SCEE-5.2-pedido-service`

### Funcionalidades

- ✅ Criar pedido
- ✅ Buscar pedido por ID
- ✅ Listar pedidos por usuário
- ✅ Listar pedidos por status
- ✅ Atualizar status do pedido
- ✅ Cancelar pedido
- ✅ Obter estatísticas
- ✅ Verificar permissão de avaliação
- ✅ Obter histórico completo

### Máquina de Estados

```
PENDENTE → PROCESSANDO → ENVIADO → ENTREGUE
   ↓            ↓
CANCELADO   CANCELADO
```

### Validações Básicas

- Pedido deve ter pelo menos um item
- Tipo de pagamento válido: CARTAO, BOLETO, PIX
- Quantidade e preço maiores que zero

### Validações Avançadas

- **Transições de Status:** Valida se transição é permitida
- **Cancelamento:**
  - Só permite em status PENDENTE ou PROCESSANDO
  - Limite de 24 horas após criação
  - Valida propriedade do pedido
- **Permissões:** Verifica se usuário pode cancelar/avaliar

### Exceções

- `PedidoServiceError` - Erro genérico
- `StatusInvalidoError` - Status inválido
- `TransicaoStatusInvalidaError` - Transição não permitida
- `PedidoNaoEncontradoError` - Pedido não encontrado
- `CancelamentoNaoPermitidoError` - Cancelamento negado

### Exemplo de Uso

```python
from repositories.pedido_repository import PedidoRepository
from repositories.produto_repository import ProdutoRepository
from repositories.usuario_repository import UsuarioRepository
from src.services.pedido_service import PedidoService
from config.database import get_connection

pedido_repo = PedidoRepository(get_connection)
produto_repo = ProdutoRepository(get_connection)
usuario_repo = UsuarioRepository(get_connection)

service = PedidoService(pedido_repo, produto_repo, usuario_repo)

# Criar pedido
pedido = service.criar_pedido(
    usuario_id=1,
    endereco_id=1,
    itens=[
        {'produto_id': 10, 'quantidade': 2, 'preco_unitario': 99.90}
    ],
    tipo_pagamento='CARTAO',
    frete=15.00
)

# Atualizar status
service.atualizar_status(pedido['id'], 'PROCESSANDO')

# Cancelar pedido
service.cancelar_pedido(pedido['id'], usuario_id=1, motivo='Desistência')
```

---

## 🏪 CatalogoService

**Branch:** `feature/SCEE-5.3-catalogo-service`

### Funcionalidades

- ✅ Buscar produtos com filtros múltiplos
- ✅ Paginação robusta
- ✅ Buscar produto por ID/SKU
- ✅ Listar categorias
- ✅ Listar produtos por categoria
- ✅ Validar disponibilidade
- ✅ Obter produtos em destaque
- ✅ Buscar produtos relacionados
- ✅ Obter faixa de preços

### Validações Básicas

- Termo de busca: mínimo 2 caracteres
- Página: maior que zero
- Itens por página: 1 a 100

### Validações Avançadas

- **Filtros:**
  - Preço mínimo: R$ 0,01
  - Preço máximo: R$ 999.999,99
  - Validação de categoria existente
  - Preço mínimo ≤ preço máximo
- **Paginação:**
  - Metadados completos (tem_proxima, tem_anterior)
  - Controle de offset/limit
- **Enriquecimento:** Adiciona dados de categoria aos produtos

### Exceções

- `CatalogoServiceError` - Erro genérico
- `ProdutoNaoEncontradoError` - Produto não encontrado
- `CategoriaNaoEncontradaError` - Categoria não encontrada
- `FiltrosInvalidosError` - Filtros inválidos

### Exemplo de Uso

```python
from repositories.produto_repository import ProdutoRepository
from repositories.categoria_repository import CategoriaRepository
from src.services.catalogo_service import CatalogoService
from config.database import get_connection

produto_repo = ProdutoRepository(get_connection)
categoria_repo = CategoriaRepository(get_connection)

service = CatalogoService(produto_repo, categoria_repo)

# Buscar produtos
resultado = service.buscar_produtos(
    termo='notebook',
    categoria_id=1,
    preco_min=1000.00,
    preco_max=5000.00,
    pagina=1,
    itens_por_pagina=20
)

print(f"Encontrados {len(resultado['produtos'])} produtos")
print(f"Página {resultado['paginacao']['pagina_atual']}")
print(f"Tem próxima: {resultado['paginacao']['tem_proxima']}")

# Produtos em destaque
destaques = service.obter_destaques(limite=10)
```

---

## 👤 UsuarioService

**Branch:** `feature/SCEE-5.4-usuario-service`

### Funcionalidades

- ✅ Buscar usuário por ID/email
- ✅ Atualizar perfil
- ✅ Alterar senha
- ✅ Resetar senha (admin)
- ✅ Promover a administrador
- ✅ Rebaixar de administrador
- ✅ Listar usuários
- ✅ Obter estatísticas
- ✅ Validar credenciais
- ✅ Verificar permissões

### Validações Básicas

- Nome: 3 a 200 caracteres
- Email: formato válido (regex)
- Senha: 8 a 128 caracteres

### Validações Avançadas

- **Email:** Pattern regex completo
- **Senha:**
  - Mínimo 8 caracteres
  - Deve conter letra e número
  - Nova senha diferente da atual
- **Permissões:**
  - Só pode editar próprio perfil ou ser admin
  - Admin não pode rebaixar a si mesmo
- **Segurança:** Remove senha_hash de respostas

### Exceções

- `UsuarioServiceError` - Erro genérico
- `UsuarioNaoEncontradoError` - Usuário não encontrado
- `EmailInvalidoError` - Email inválido
- `SenhaFracaError` - Senha não atende requisitos
- `PermissaoNegadaError` - Sem permissão

### Exemplo de Uso

```python
from repositories.usuario_repository import UsuarioRepository
from repositories.endereco_repository import EnderecoRepository
from src.services.usuario_service import UsuarioService
from config.database import get_connection

usuario_repo = UsuarioRepository(get_connection)
endereco_repo = EnderecoRepository(get_connection)

service = UsuarioService(usuario_repo, endereco_repo)

# Atualizar perfil
usuario = service.atualizar_perfil(
    usuario_id=1,
    nome='João Silva',
    email='joao.silva@email.com',
    usuario_solicitante_id=1
)

# Alterar senha
service.alterar_senha(
    usuario_id=1,
    senha_atual='senhaAntiga123',
    nova_senha='novaSenha456'
)

# Promover a admin (requer permissão de admin)
service.promover_a_admin(usuario_id=5, usuario_admin_id=1)
```

---

## 📧 EmailService

**Branch:** `feature/SCEE-5.5-email-service`

### Funcionalidades

- ✅ Enviar email simples
- ✅ Enviar email com template
- ✅ Email de boas-vindas
- ✅ Email de confirmação de pedido
- ✅ Email de atualização de status
- ✅ Email de reset de senha
- ✅ Envio em lote
- ✅ Fila de emails com priorização
- ✅ Retry logic
- ✅ Histórico de envios

### Templates Disponíveis

- `BEM_VINDO` - Boas-vindas a novos usuários
- `CONFIRMACAO_PEDIDO` - Confirmação de pedido
- `ATUALIZACAO_PEDIDO` - Atualização genérica
- `PEDIDO_ENVIADO` - Pedido enviado
- `PEDIDO_ENTREGUE` - Pedido entregue
- `PEDIDO_CANCELADO` - Pedido cancelado
- `RESETAR_SENHA` - Reset de senha
- `NOTIFICACAO_GERAL` - Notificação genérica

### Validações Básicas

- Email: formato válido (regex)
- Assunto: não vazio
- Corpo: não vazio

### Validações Avançadas

- **Retry Logic:**
  - Máximo 3 tentativas
  - Timeout de 30 segundos
- **Limites:**
  - Máximo 50 emails por lote
- **Fila:**
  - Priorização (1-10)
  - Processamento controlado
- **Modo Mock:** Para desenvolvimento sem envio real

### Exceções

- `EmailServiceError` - Erro genérico
- `EmailInvalidoError` - Email inválido
- `TemplateNaoEncontradoError` - Template não encontrado
- `EnvioEmailError` - Erro no envio

### Exemplo de Uso

```python
from src.services.email_service import EmailService, TipoEmail

service = EmailService(
    remetente='noreply@scee.com.br',
    modo_mock=True  # True para desenvolvimento
)

# Email simples
service.enviar_email(
    destinatario='cliente@email.com',
    assunto='Bem-vindo!',
    corpo='Olá, bem-vindo ao SCEE!'
)

# Email com template
service.enviar_email_template(
    destinatario='cliente@email.com',
    tipo=TipoEmail.BEM_VINDO,
    dados={'nome': 'João Silva'}
)

# Confirmação de pedido
service.enviar_confirmacao_pedido(
    usuario={'email': 'cliente@email.com', 'nome': 'João'},
    pedido={'id': 123, 'total': 299.90, 'itens': []}
)

# Processar fila
resultado = service.processar_fila(limite=10)
print(f"Processados: {resultado['processados']}")
```

---

## 📊 Resumo das Implementações

### Estatísticas

| Service | Linhas | Métodos Públicos | Exceções | Validações |
|---------|--------|------------------|----------|------------|
| CarrinhoService | 390 | 8 | 4 | 8 |
| PedidoService | 422 | 11 | 4 | 5 |
| CatalogoService | 450 | 12 | 3 | 7 |
| UsuarioService | 467 | 13 | 4 | 6 |
| EmailService | 564 | 12 | 3 | 3 |
| **TOTAL** | **2.293** | **56** | **18** | **29** |

### Padrões Utilizados

1. **Dependency Injection:** Todos os services recebem repositórios via construtor
2. **Exception Hierarchy:** Exceções customizadas herdando de base
3. **Validação em Camadas:** Validações básicas e avançadas separadas
4. **Constants:** Limites e constantes definidas como atributos de classe
5. **Type Hints:** Tipagem completa em todos os métodos
6. **Documentação:** Docstrings detalhadas com Args/Returns/Raises

### Próximos Passos

1. **Testes Unitários:** Criar testes para cada service
2. **Integração:** Conectar services com Views (GUI)
3. **Merge:** Fazer merge das branches após revisão
4. **Deploy:** Preparar para produção

---

## 🔗 Branches

Todas as implementações estão em branches separadas:

```bash
git checkout feature/SCEE-5.1-carrinho-service
git checkout feature/SCEE-5.2-pedido-service
git checkout feature/SCEE-5.3-catalogo-service
git checkout feature/SCEE-5.4-usuario-service
git checkout feature/SCEE-5.5-email-service
```

Para fazer merge de uma branch:

```bash
git checkout main
git merge feature/SCEE-5.X-nome-service
git push origin main
```
