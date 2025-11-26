# ✅ Migração para MySQL/MariaDB Concluída

## 🎯 Resumo da Migração

O projeto SCEE foi completamente migrado de SQLite para MySQL/MariaDB conforme solicitado.

### ✅ Concluído

1. **Dependências Python** (`requirements.txt`)
   - ✅ Adicionado `pymysql==1.1.0`
   - ✅ Adicionado `cryptography==41.0.7`
   - ✅ Adicionado `sqlalchemy==2.0.23`

2. **Configuração de Conexão** (`config/database.py`)
   - ✅ Substituído `sqlite3` por `pymysql`
   - ✅ Configurado para usar variáveis de ambiente
   - ✅ Implementado `get_connection()` com DictCursor
   - ✅ Adaptado `init_db()` para MySQL (sem executescript)
   - ✅ Adaptado `reset_db()` com comandos MySQL

3. **Settings** (`config/settings.py`)
   - ✅ Adicionados campos MySQL: `mysql_host`, `mysql_port`, `mysql_user`, `mysql_password`, `mysql_database`
   - ✅ Atualizado `database_url` para: `mysql+pymysql://scee_user:scee_pass@localhost:13306/SCEE`

4. **Schema SQL** (`schema/schema.sql`)
   - ✅ Convertido de SQLite para MySQL/MariaDB
   - ✅ `INTEGER PRIMARY KEY AUTOINCREMENT` → `INT AUTO_INCREMENT PRIMARY KEY`
   - ✅ `TEXT` → `VARCHAR(n)` onde apropriado
   - ✅ `REAL` → `DECIMAL(10, 2)` para valores monetários
   - ✅ `DATETIME` → `TIMESTAMP` com `ON UPDATE CURRENT_TIMESTAMP`
   - ✅ `CHECK(campo IN (...))` → `ENUM(...)`
   - ✅ `BOOLEAN` mantido (MariaDB converte para TINYINT(1))
   - ✅ Adicionado `ENGINE=InnoDB DEFAULT CHARSET=utf8mb4`
   - ✅ Índices criados inline nas tabelas
   - ✅ 4 Views criadas: `vw_produtos_completos`, `vw_clientes_completos`, `vw_pedidos_detalhados`, `vw_carrinhos_totais`

5. **Seed SQL** (`seed/seed.sql`)
   - ✅ Convertido de SQLite para MySQL
   - ✅ `INSERT OR IGNORE` → `INSERT IGNORE`
   - ✅ Mantidos os mesmos dados de teste

6. **Docker** (`compose.yaml`)
   - ✅ MariaDB já estava configurado (porta 13306)
   - ✅ Adminer configurado (porta 8080) - conflito de porta, mas MariaDB funcionando

7. **Arquivos Criados**
   - ✅ `.env.example` - Exemplo de variáveis de ambiente
   - ✅ `test_mysql.py` - Script de teste e gerenciamento do banco
   - ✅ `MYSQL_README.md` - Documentação completa do MySQL
   - ✅ `schema/triggers.sql` - Triggers separados (para criação manual)
   - ✅ `MIGRACAO_MYSQL.md` - Este arquivo

## 🗄️ Banco de Dados

### Tabelas (11)
1. `usuarios` - 2 registros ✅
2. `clientes_info` - 1 registro ✅
3. `administradores` - 1 registro ✅
4. `enderecos` - 1 registro ✅
5. `categorias` - 5 registros ✅
6. `produtos` - 15 registros ✅
7. `imagens_produto` - 16 registros ✅
8. `carrinhos` - 0 registros ✅
9. `itens_carrinho` - 0 registros ✅
10. `pedidos` - 0 registros ✅
11. `itens_pedido` - 0 registros ✅

### Views (4)
1. `vw_produtos_completos` ✅
2. `vw_clientes_completos` ✅
3. `vw_pedidos_detalhados` ✅
4. `vw_carrinhos_totais` ✅

### Triggers (3) - Para criar manualmente
1. `validate_estoque_carrinho` ⏳ (requer DELIMITER)
2. `abater_estoque_pedido` ⏳ (requer DELIMITER)
3. `devolver_estoque_pedido` ⏳ (requer DELIMITER)

**Nota:** Os triggers estão em `schema/triggers.sql` e devem ser criados manualmente via MySQL CLI ou Adminer, pois o PyMySQL não suporta `DELIMITER`.

## 🚀 Como Usar

### 1. Iniciar MariaDB
```bash
docker compose up -d
```

### 2. Criar Schema (já feito)
```bash
python test_mysql.py
# Opção 2 ou 3
```

### 3. Popular com Dados (já feito)
```bash
docker exec -i mariadb_scee mariadb -uscee_user -pscee_pass SCEE < seed/seed.sql
```

### 4. Verificar
```bash
python test_mysql.py
# Opção 1 ou 4
```

## 📝 Próximos Passos

### ⏳ Pendentes
1. **Atualizar Repositories** - Converter de `sqlite3.Row` para `pymysql.DictCursor`
   - `repositories/base_repository.py`
   - `repositories/usuario_repository.py`
   - `repositories/cliente_repository.py`
   - `repositories/endereco_repository.py`
   - `repositories/categoria_repository.py`
   - `repositories/produto_repository.py`
   - `repositories/carrinho_repository.py`
   - `repositories/pedido_repository.py`

2. **Criar Triggers** - Via MySQL CLI ou Adminer
   ```sql
   -- Usar o arquivo schema/triggers.sql
   ```

3. **Testar CRUD** - Testar todas as operações dos repositories

4. **Implementar API FastAPI** - Criar endpoints REST

5. **Testes de Integração** - Garantir funcionamento completo

## 🔍 Verificação

```bash
# Testar conexão
python test_mysql.py

# Ver dados no Adminer
# http://localhost:8080 (se porta 8080 estiver livre)

# MySQL CLI
docker exec -it mariadb_scee mariadb -uscee_user -pscee_pass SCEE

# Queries de verificação
SELECT COUNT(*) FROM usuarios;
SELECT * FROM vw_produtos_completos LIMIT 5;
SHOW TABLES;
SHOW FULL TABLES WHERE Table_type = 'VIEW';
```

## 🎓 Usuários de Teste

### Administrador
- Email: `admin@scee.com`
- Senha: `admin123`

### Cliente
- Email: `joao@email.com`
- Senha: `cliente123`
- CPF: 123.456.789-00
- Telefone: (11) 98765-4321

## 🔧 Conexão MySQL

- **Host:** localhost
- **Porta:** 13306
- **Usuário:** scee_user
- **Senha:** scee_pass
- **Database:** SCEE

## 📊 Status da Migração

| Item | Status |
|------|--------|
| requirements.txt | ✅ Concluído |
| config/database.py | ✅ Concluído |
| config/settings.py | ✅ Concluído |
| schema/schema.sql | ✅ Concluído |
| seed/seed.sql | ✅ Concluído |
| .env.example | ✅ Concluído |
| MariaDB Container | ✅ Rodando |
| Tabelas Criadas | ✅ 11/11 |
| Views Criadas | ✅ 4/4 |
| Dados Seed | ✅ Populado |
| Triggers | ⏳ Pendente (manual) |
| Repositories | ⏳ Próximo passo |
| API FastAPI | ⏳ Futuro |
| Testes | ⏳ Futuro |

---

**Data da Migração:** $(date)
**Versão MySQL:** 12.0.2-MariaDB-ubu2404
**Status:** ✅ Migração de Banco Concluída - Próximo: Atualizar Repositories
