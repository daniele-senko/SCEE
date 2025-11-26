# 🧪 Guia de Testes - Services SCEE

Este documento explica como testar todos os services implementados.

## 📋 Índice

1. [Pré-requisitos](#pré-requisitos)
2. [Testes Manuais](#testes-manuais)
3. [Testes Unitários](#testes-unitários)
4. [Testes de Integração](#testes-de-integração)
5. [Comandos Úteis](#comandos-úteis)

---

## 🔧 Pré-requisitos

### 1. Instalar dependências de teste

```bash
pip install pytest pytest-cov pytest-mock
```

### 2. Garantir banco de dados populado

```bash
# Inicializar banco
python init_db.py

# Popular com dados de teste
python warmup_database.py
```

### 3. Verificar configuração

```bash
# Testar conexão
python tests/test_connection.py
```

---

## 🖐️ Testes Manuais

### Opção 1: Script Interativo

Execute o script de teste manual que demonstra todas as funcionalidades:

```bash
python test_services_manual.py
```

Este script irá:
- ✅ Testar CarrinhoService (adicionar, remover, validar)
- ✅ Testar PedidoService (criar, atualizar status, cancelar)
- ✅ Testar CatalogoService (buscar, filtrar, listar)
- ✅ Testar UsuarioService (buscar, atualizar, permissões)
- ✅ Testar EmailService (enviar, templates, fila)

### Opção 2: Console Python

```python
# Inicie o Python
python

# CarrinhoService
from config.database import get_connection
from repositories.carrinho_repository import CarrinhoRepository
from repositories.produto_repository import ProdutoRepository
from src.services.carrinho_service import CarrinhoService

carrinho_repo = CarrinhoRepository(get_connection)
produto_repo = ProdutoRepository(get_connection)
service = CarrinhoService(carrinho_repo, produto_repo)

# Adicionar item
item = service.adicionar_item(usuario_id=1, produto_id=1, quantidade=2)
print(item)

# Listar itens
itens = service.listar_itens(usuario_id=1)
print(itens)

# Calcular total
total = service.calcular_total(usuario_id=1)
print(f"Total: R$ {total:.2f}")
```

### Opção 3: Jupyter Notebook

Crie um notebook para testes interativos:

```bash
pip install jupyter
jupyter notebook
```

Crie células com os exemplos acima.

---

## 🧪 Testes Unitários

### Estrutura dos Testes

```
tests/
├── services/
│   ├── test_carrinho_service.py    ✅ Implementado
│   ├── test_pedido_service.py      🔜 A criar
│   ├── test_catalogo_service.py    🔜 A criar
│   ├── test_usuario_service.py     🔜 A criar
│   └── test_email_service.py       🔜 A criar
└── ...
```

### Executar Testes Unitários

#### Todos os testes

```bash
# Executar todos os testes
pytest tests/services/ -v

# Com cobertura
pytest tests/services/ --cov=src/services --cov-report=html
```

#### Teste específico

```bash
# Testar apenas CarrinhoService
pytest tests/services/test_carrinho_service.py -v

# Testar um método específico
pytest tests/services/test_carrinho_service.py::TestCarrinhoService::test_adicionar_item_sucesso -v

# Modo verbose com detalhes
pytest tests/services/test_carrinho_service.py -vv
```

#### Ver cobertura

```bash
# Gerar relatório de cobertura
pytest tests/services/ --cov=src/services --cov-report=term-missing

# Gerar HTML
pytest tests/services/ --cov=src/services --cov-report=html
# Abrir: htmlcov/index.html
```

### Exemplo de Teste Unitário

```python
def test_adicionar_item_sucesso(service, mock_carrinho_repo, mock_produto_repo):
    """Testa adição de item com sucesso."""
    # Arrange (Preparar)
    mock_produto_repo.buscar_por_id.return_value = {
        'id': 1, 'nome': 'Notebook', 'preco': 2500.00,
        'estoque': 10, 'ativo': True
    }
    
    # Act (Executar)
    resultado = service.adicionar_item(usuario_id=1, produto_id=1, quantidade=2)
    
    # Assert (Verificar)
    assert resultado is not None
    assert resultado['quantidade'] == 2
```

---

## 🔗 Testes de Integração

Testes que usam o banco de dados real.

### Criar Teste de Integração

```python
# tests/integration/test_carrinho_integration.py
import pytest
from config.database import get_connection, reset_db
from repositories.carrinho_repository import CarrinhoRepository
from repositories.produto_repository import ProdutoRepository
from src.services.carrinho_service import CarrinhoService

@pytest.fixture(scope='module')
def db():
    """Prepara banco de teste."""
    reset_db()  # Limpa e recria
    # Popular dados de teste
    yield
    # Limpar após testes

def test_carrinho_fluxo_completo(db):
    """Testa fluxo completo de carrinho."""
    carrinho_repo = CarrinhoRepository(get_connection)
    produto_repo = ProdutoRepository(get_connection)
    service = CarrinhoService(carrinho_repo, produto_repo)
    
    # Adicionar item
    item = service.adicionar_item(usuario_id=1, produto_id=1, quantidade=2)
    assert item['quantidade'] == 2
    
    # Verificar no banco
    itens = service.listar_itens(usuario_id=1)
    assert len(itens) > 0
    
    # Limpar
    service.limpar_carrinho(usuario_id=1)
    itens = service.listar_itens(usuario_id=1)
    assert len(itens) == 0
```

### Executar Integração

```bash
pytest tests/integration/ -v
```

---

## 🛠️ Comandos Úteis

### Desenvolvimento

```bash
# Executar testes ao salvar arquivo
pytest-watch tests/services/

# Executar apenas testes que falharam
pytest --lf

# Parar no primeiro erro
pytest -x

# Mostrar prints durante testes
pytest -s
```

### Análise

```bash
# Testes mais lentos
pytest --durations=10

# Modo detalhado
pytest -vv

# Apenas nomes dos testes
pytest --collect-only
```

### Debug

```bash
# Entrar em debug ao falhar
pytest --pdb

# Traceback completo
pytest --tb=long

# Sem captura de output
pytest -s --tb=short
```

---

## 📊 Cobertura de Código

### Meta de Cobertura

- **Mínimo:** 80%
- **Ideal:** 90%+

### Gerar Relatório Completo

```bash
# Terminal
pytest tests/services/ --cov=src/services --cov-report=term-missing

# HTML interativo
pytest tests/services/ --cov=src/services --cov-report=html
open htmlcov/index.html

# XML (para CI/CD)
pytest tests/services/ --cov=src/services --cov-report=xml
```

### Interpretar Cobertura

```
Name                              Stmts   Miss  Cover   Missing
---------------------------------------------------------------
src/services/carrinho_service.py    150     15    90%   45-50, 120
src/services/pedido_service.py      200     30    85%   78-82, 150-165
```

- **Stmts:** Total de linhas executáveis
- **Miss:** Linhas não executadas
- **Cover:** Percentual de cobertura
- **Missing:** Linhas específicas não cobertas

---

## ✅ Checklist de Testes

### Por Service

- [ ] **CarrinhoService**
  - [x] Testes unitários criados
  - [ ] Cobertura > 80%
  - [ ] Testes de integração
  - [ ] Documentação atualizada

- [ ] **PedidoService**
  - [ ] Testes unitários criados
  - [ ] Cobertura > 80%
  - [ ] Testes de integração
  - [ ] Documentação atualizada

- [ ] **CatalogoService**
  - [ ] Testes unitários criados
  - [ ] Cobertura > 80%
  - [ ] Testes de integração
  - [ ] Documentação atualizada

- [ ] **UsuarioService**
  - [ ] Testes unitários criados
  - [ ] Cobertura > 80%
  - [ ] Testes de integração
  - [ ] Documentação atualizada

- [ ] **EmailService**
  - [ ] Testes unitários criados
  - [ ] Cobertura > 80%
  - [ ] Testes de integração
  - [ ] Documentação atualizada

### Casos de Teste Essenciais

#### CarrinhoService
- [x] Adicionar item válido
- [x] Adicionar com quantidade inválida
- [x] Adicionar produto inexistente
- [x] Adicionar produto inativo
- [x] Adicionar com estoque insuficiente
- [x] Exceder limite de itens
- [x] Remover item
- [x] Atualizar quantidade
- [x] Calcular total
- [x] Validar carrinho
- [x] Limpar carrinho

#### PedidoService
- [ ] Criar pedido válido
- [ ] Criar com dados inválidos
- [ ] Atualizar status válido
- [ ] Transição inválida
- [ ] Cancelar permitido
- [ ] Cancelar não permitido
- [ ] Obter estatísticas
- [ ] Histórico completo

#### CatalogoService
- [ ] Buscar produtos
- [ ] Filtrar por categoria
- [ ] Filtrar por preço
- [ ] Paginação
- [ ] Produtos em destaque
- [ ] Produtos relacionados
- [ ] Validar disponibilidade

#### UsuarioService
- [ ] Buscar usuário
- [ ] Atualizar perfil
- [ ] Alterar senha
- [ ] Resetar senha
- [ ] Promover/rebaixar
- [ ] Validar permissões

#### EmailService
- [ ] Enviar email simples
- [ ] Enviar com template
- [ ] Validar email
- [ ] Fila de emails
- [ ] Retry logic
- [ ] Histórico

---

## 🚀 Executar Testes Completos

### Comando All-in-One

```bash
# Testes + Cobertura + Relatório HTML
pytest tests/services/ -v \
  --cov=src/services \
  --cov-report=html \
  --cov-report=term-missing \
  --cov-fail-under=80
```

### CI/CD Pipeline

```yaml
# .github/workflows/tests.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      - name: Run tests
        run: |
          pytest tests/ --cov=src --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

---

## 📚 Recursos

### Documentação

- [Pytest](https://docs.pytest.org/)
- [Coverage.py](https://coverage.readthedocs.io/)
- [Pytest-mock](https://pytest-mock.readthedocs.io/)

### Tutoriais

- [Real Python - Testing](https://realpython.com/pytest-python-testing/)
- [Pytest Good Practices](https://docs.pytest.org/en/latest/goodpractices.html)

---

## 💡 Dicas

1. **Escreva testes antes de corrigir bugs** - Test-Driven Bug Fixing
2. **Use fixtures para código reutilizável** - DRY (Don't Repeat Yourself)
3. **Teste casos extremos** - Valores nulos, negativos, muito grandes
4. **Mock dependências externas** - Banco, APIs, sistema de arquivos
5. **Mantenha testes rápidos** - Testes lentos são testes ignorados
6. **Um assert por teste** (quando possível) - Testes mais claros
7. **Nomes descritivos** - `test_adicionar_item_com_estoque_insuficiente`

---

## ⚠️ Problemas Comuns

### "ModuleNotFoundError"

```bash
# Adicione ao path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### "No tests collected"

```bash
# Verifique que arquivo começa com test_
# Verifique que função começa com test_
```

### "Fixture not found"

```bash
# Instale pytest-mock
pip install pytest-mock
```

### Banco de dados em uso

```bash
# Pare containers Docker
docker-compose down

# Limpe banco de teste
python init_db.py --reset
```
