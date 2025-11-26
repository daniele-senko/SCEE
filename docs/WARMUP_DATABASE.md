# 🔥 Database Warmup - Script de Aquecimento do Banco

## 📋 Descrição

Script Python para **aquecer e validar** o banco de dados MySQL do SCEE, testando todos os repositories com operações CRUD completas.

## 🎯 Objetivo

- ✅ Validar conexões com banco de dados
- ✅ Testar performance dos repositories
- ✅ Verificar integridade de foreign keys
- ✅ Garantir que todas as operações CRUD funcionam
- ✅ Detectar problemas antes de deploy

## 🚀 Como Executar

```bash
# Na raiz do projeto
python warmup_database.py
```

## 📊 O que é Testado

### 1. UsuarioRepository
- ✅ Create (salvar)
- ✅ Read por ID
- ✅ Read por Email
- ✅ Update
- ✅ List com paginação

### 2. CategoriaRepository
- ✅ Create
- ✅ Read por ID
- ✅ Update
- ✅ List

### 3. ProdutoRepository
- ✅ Create
- ✅ Read por ID
- ✅ Read por SKU
- ✅ Update (preço e estoque)
- ✅ List com paginação
- ✅ Busca com filtros

### 4. ClienteRepository
- ✅ Create
- ✅ Read por ID
- ✅ Read por usuário
- ✅ Update

### 5. EnderecoRepository
- ✅ Create
- ✅ Read por ID
- ✅ List por usuário
- ✅ Update

### 6. CarrinhoRepository
- ✅ Create/Obter carrinho
- ✅ Adicionar item
- ✅ Listar itens
- ✅ Calcular total
- ✅ Atualizar quantidade
- ✅ Remover item
- ✅ Limpar carrinho

### 7. PedidoRepository
- ✅ Create
- ✅ Adicionar item
- ✅ Read por ID
- ✅ Listar itens
- ✅ Atualizar status
- ✅ Listar por usuário

## 🔄 Fluxo de Execução

```
1. Inicialização
   └─> Conecta com banco
   └─> Inicializa 7 repositories

2. Testes (em ordem)
   └─> UsuarioRepository
   └─> CategoriaRepository
   └─> ProdutoRepository
   └─> ClienteRepository
   └─> EnderecoRepository
   └─> CarrinhoRepository
   └─> PedidoRepository

3. Limpeza Automática
   └─> Remove dados de teste
   └─> Respeita foreign keys
   └─> Logs detalhados
```

## 📝 Exemplo de Output

```
================================================================================
INICIANDO AQUECIMENTO DO BANCO DE DADOS
================================================================================

--------------------------------------------------------------------------------
🔄 Testando UsuarioRepository
--------------------------------------------------------------------------------
📝 Criando usuário: warmup_1234567890@teste.com
✅ Usuário criado com ID: 42
🔍 Buscando usuário por ID: 42
✅ Usuário encontrado: Teste Warmup
📝 Atualizando usuário: Teste Warmup Atualizado
✅ Usuário atualizado
📋 Listando usuários (limit 5)
✅ 3 usuários listados

... (continua para todos os repositories)

================================================================================
✅ AQUECIMENTO CONCLUÍDO COM SUCESSO!
================================================================================

================================================================================
🧹 LIMPANDO DADOS DE TESTE
================================================================================
🗑️ Removendo 1 registro(s) de pedidos
  ✅ pedidos ID 1 removido
🗑️ Removendo 1 registro(s) de carrinhos
  ✅ carrinhos ID 1 removido
... (continua)
✅ Limpeza concluída
```

## ⚙️ Requisitos

- Python 3.9+
- MySQL/MariaDB rodando (Docker Compose)
- Dependências instaladas (`requirements.txt`)
- Banco de dados inicializado

## 🔧 Configuração

O script usa as mesmas configurações do projeto:
- `.env` - Credenciais do banco
- `config/database.py` - Factory de conexão
- Todos os repositories do projeto

## 🎭 Casos de Uso

### 1. Validação Pré-Deploy
```bash
# Antes de fazer deploy, validar banco
python warmup_database.py
# Se retornar 0, está tudo OK
echo $?
```

### 2. Teste de Performance
```bash
# Medir tempo de execução
time python warmup_database.py
```

### 3. CI/CD Pipeline
```yaml
# .github/workflows/test.yml
- name: Warmup Database
  run: python warmup_database.py
```

### 4. Debugging
```bash
# Com logs detalhados
python warmup_database.py 2>&1 | tee warmup.log
```

## 🛡️ Segurança

- ✅ Dados criados são **temporários**
- ✅ Limpeza **automática** garantida (finally block)
- ✅ Não afeta dados existentes
- ✅ IDs únicos com timestamp
- ✅ Transações isoladas

## ⚠️ Avisos

- **Não execute em produção** sem supervisão
- Script cria e deleta dados no banco
- Requer permissões de INSERT, UPDATE, DELETE
- Logs podem conter informações sensíveis

## 🐛 Troubleshooting

### Erro: "ModuleNotFoundError"
```bash
# Instalar dependências
pip install -r requirements.txt
```

### Erro: "Can't connect to MySQL"
```bash
# Verificar Docker
docker ps | grep mariadb
# Iniciar banco
docker-compose up -d
```

### Erro: "Foreign key constraint fails"
```bash
# Verificar schema
mysql -h localhost -P 13306 -u scee_user -p
USE SCEE;
SHOW TABLES;
```

## 📈 Métricas

Em uma execução típica:
- **Tempo**: ~1-2 segundos
- **Registros criados**: ~10-15
- **Operações**: ~50+ queries
- **Repositórios testados**: 7

## 🔗 Referências

- [Documentação MySQL](https://dev.mysql.com/doc/)
- [PyMySQL](https://pymysql.readthedocs.io/)
- [SCEE Repositories](./ESTRUTURA.md)

---

**Última atualização**: 25/11/2025  
**Versão**: 1.0.0  
**Status**: ✅ Produção
