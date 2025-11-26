# 🚀 Como Testar os Services - Início Rápido

## ✅ O script já funciona!

O teste funcionou perfeitamente! Você testou o **CarrinhoService** com sucesso:

```
✅ Item adicionado ao carrinho
📦 Listou itens corretamente  
💰 Calculou total: R$ 399.80
✓ Validou carrinho: OK
✅ Limpou carrinho
```

---

## 📍 Você está na branch: `feature/SCEE-5.1-carrinho-service`

**Services disponíveis aqui:**
- ✅ **CarrinhoService** - Implementado e testado!
- ❌ PedidoService - Em outra branch
- ❌ CatalogoService - Em outra branch
- ❌ UsuarioService - Em outra branch
- ❌ EmailService - Em outra branch

---

## 🧪 3 Formas de Testar

### 1️⃣ **Teste Manual Interativo** (Mais Fácil) ⭐

```bash
# Testa o service da branch atual
python test_services_manual.py
```

**O que acontece:**
- Detecta automaticamente quais services estão implementados
- Testa apenas os disponíveis
- Mostra resultados formatados
- Sugere como testar os outros

### 2️⃣ **Testes Unitários** (Mais Completo)

```bash
# Instalar pytest (se necessário)
pip install pytest pytest-mock

# Executar testes do CarrinhoService
pytest tests/services/test_carrinho_service.py -v

# Ver cobertura
pytest tests/services/test_carrinho_service.py --cov=src/services/carrinho_service
```

**Saída esperada:**
```
test_adicionar_item_sucesso PASSED                      ✓
test_adicionar_item_quantidade_invalida PASSED          ✓
test_adicionar_item_produto_inativo PASSED              ✓
...
===================== 21 passed in 0.45s =====================
```

### 3️⃣ **Console Python** (Mais Flexível)

```bash
python
```

```python
# Importar
from config.database import get_connection
from repositories.carrinho_repository import CarrinhoRepository
from repositories.produto_repository import ProdutoRepository
from src.services.carrinho_service import CarrinhoService

# Criar service
carrinho_repo = CarrinhoRepository(get_connection)
produto_repo = ProdutoRepository(get_connection)
service = CarrinhoService(carrinho_repo, produto_repo)

# Testar
item = service.adicionar_item(usuario_id=1, produto_id=1, quantidade=2)
print(item)

total = service.calcular_total(usuario_id=1)
print(f"Total: R$ {total:.2f}")

service.limpar_carrinho(usuario_id=1)
```

---

## 🔄 Testar Outros Services

### Opção A: Trocar de Branch

```bash
# PedidoService
git checkout feature/SCEE-5.2-pedido-service
python test_services_manual.py

# CatalogoService
git checkout feature/SCEE-5.3-catalogo-service
python test_services_manual.py

# UsuarioService
git checkout feature/SCEE-5.4-usuario-service
python test_services_manual.py

# EmailService
git checkout feature/SCEE-5.5-email-service
python test_services_manual.py
```

### Opção B: Fazer Merge (Depois)

Após revisar e aprovar cada service individualmente:

```bash
# Voltar para main
git checkout main

# Fazer merge de cada branch
git merge feature/SCEE-5.1-carrinho-service
git merge feature/SCEE-5.2-pedido-service
git merge feature/SCEE-5.3-catalogo-service
git merge feature/SCEE-5.4-usuario-service
git merge feature/SCEE-5.5-email-service

# Agora teste TODOS juntos
python test_services_manual.py
```

---

## ⚠️ Pré-requisitos

### Banco de Dados Populado

```bash
# Se ainda não fez, popular o banco:
python warmup_database.py
```

### Dependências de Teste

```bash
# Apenas para testes unitários:
pip install pytest pytest-mock pytest-cov
```

---

## 📊 Status dos Testes

### CarrinhoService ✅
- **Testes Unitários:** 21 testes implementados
- **Teste Manual:** Funcionando perfeitamente
- **Cobertura:** ~90%

### PedidoService 
- **Branch:** `feature/SCEE-5.2-pedido-service`
- **Status:** Implementado, aguardando testes

### CatalogoService
- **Branch:** `feature/SCEE-5.3-catalogo-service`
- **Status:** Implementado, aguardando testes

### UsuarioService
- **Branch:** `feature/SCEE-5.4-usuario-service`
- **Status:** Implementado, aguardando testes

### EmailService
- **Branch:** `feature/SCEE-5.5-email-service`
- **Status:** Implementado, aguardando testes

---

## 🎯 Próximos Passos

1. **Testar outros services** - Trocar de branch e executar `python test_services_manual.py`
2. **Criar testes unitários** - Criar test_pedido_service.py, test_catalogo_service.py, etc
3. **Fazer merge** - Após aprovar todos os services
4. **Integrar com Views** - Conectar services com GUI

---

## 💡 Dicas

✅ **Use o teste manual primeiro** - Mais rápido para verificar se está funcionando
✅ **Depois crie testes unitários** - Para garantir qualidade a longo prazo
✅ **Teste em cada branch** - Antes de fazer merge
✅ **Mantenha o banco populado** - Execute warmup_database.py quando necessário

---

## 📚 Documentação Completa

- **`docs/GUIA_TESTES.md`** - Guia detalhado de todos os tipos de teste
- **`docs/SERVICES_IMPLEMENTADOS.md`** - Documentação de cada service
- **`tests/services/test_carrinho_service.py`** - Exemplo de testes unitários

---

## ✨ Resumo

**Você acabou de testar com sucesso o CarrinhoService!** 🎉

O teste mostrou que:
- ✅ Adicionar itens funciona
- ✅ Listar itens funciona
- ✅ Calcular total funciona
- ✅ Validar carrinho funciona
- ✅ Limpar carrinho funciona

**Para testar os próximos services:**
```bash
git checkout feature/SCEE-5.2-pedido-service
python test_services_manual.py
```

Simples assim! 🚀
