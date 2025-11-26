# Configuração MySQL/MariaDB - SCEE

## 🚀 Início Rápido

### 1. Iniciar o MariaDB com Docker

```bash
# Subir o container MariaDB
docker-compose up -d

# Verificar se está rodando
docker-compose ps
```

O MariaDB estará disponível em:
- **Host:** localhost
- **Porta:** 13306
- **Usuário:** scee_user
- **Senha:** scee_pass
- **Database:** SCEE

### 2. Configurar Variáveis de Ambiente

```bash
# Copiar o arquivo de exemplo
cp .env.example .env

# Editar conforme necessário (opcional)
nano .env
```

### 3. Instalar Dependências Python

```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt
```

### 4. Criar o Schema do Banco

```bash
# Testar conexão e criar schema
python test_mysql.py
# Escolha a opção 2 (Criar schema)

# Ou use o script init_db.py
python init_db.py
```

### 5. Popular com Dados de Teste (Seed)

```bash
# Executar o seed manualmente via MySQL CLI
docker exec -i mariadb_scee mysql -uscee_user -pscee_pass SCEE < seed/seed.sql

# Ou via Adminer (interface web)
# Acesse: http://localhost:8080
# Faça login com as credenciais acima
# SQL command > Cole o conteúdo de seed/seed.sql > Execute
```

## 🗄️ Estrutura do Banco de Dados

### Tabelas (11 tabelas)

1. **usuarios** - Tabela base para clientes e administradores
2. **clientes_info** - Informações específicas de clientes (CPF, telefone, etc)
3. **administradores** - Informações de administradores (cargo, nível de acesso)
4. **enderecos** - Endereços dos clientes
5. **categorias** - Categorias de produtos
6. **produtos** - Catálogo de produtos
7. **imagens_produto** - Imagens dos produtos
8. **carrinhos** - Carrinhos de compras ativos
9. **itens_carrinho** - Itens dentro dos carrinhos
10. **pedidos** - Pedidos realizados
11. **itens_pedido** - Itens dos pedidos

### Views (4 views)

1. **vw_produtos_completos** - Produtos com informações de categoria e imagem principal
2. **vw_clientes_completos** - Clientes com todas as informações agregadas
3. **vw_pedidos_detalhados** - Pedidos com detalhes de cliente e endereço
4. **vw_carrinhos_totais** - Carrinhos com totalizadores

### Triggers

1. **validate_estoque_carrinho** - Valida estoque antes de adicionar ao carrinho
2. **abater_estoque_pedido** - Abate estoque ao criar pedido
3. **devolver_estoque_pedido** - Devolve estoque ao cancelar pedido

## 🔧 Ferramentas Disponíveis

### Adminer (Interface Web para MySQL)

Acesse: http://localhost:8080

- **Sistema:** MySQL
- **Servidor:** mariadb_scee
- **Usuário:** scee_user
- **Senha:** scee_pass
- **Base de dados:** SCEE

### Script de Teste (test_mysql.py)

```bash
python test_mysql.py
```

Opções disponíveis:
1. Listar tabelas e views
2. Criar schema (init_db)
3. Resetar banco (reset_db + init_db)
4. Mostrar contagem de registros

## 📊 Dados Iniciais (Seed)

Após executar o seed, você terá:

- **5 categorias** (Eletrônicos, Roupas, Livros, Casa e Decoração, Esportes)
- **15 produtos** distribuídos nas categorias
- **16 imagens** de produtos
- **2 usuários:**
  - Admin: `admin@scee.com` / senha: `admin123`
  - Cliente: `joao@email.com` / senha: `cliente123`

## 🛠️ Comandos Úteis

### Docker Compose

```bash
# Iniciar serviços
docker-compose up -d

# Parar serviços
docker-compose down

# Ver logs
docker-compose logs -f mariadb_scee

# Acessar MySQL CLI
docker exec -it mariadb_scee mysql -uscee_user -pscee_pass SCEE
```

### Backup e Restore

```bash
# Backup
docker exec mariadb_scee mysqldump -uscee_user -pscee_pass SCEE > backup.sql

# Restore
docker exec -i mariadb_scee mysql -uscee_user -pscee_pass SCEE < backup.sql
```

### Consultas Úteis

```sql
-- Ver todas as tabelas
SHOW TABLES;

-- Ver todas as views
SHOW FULL TABLES WHERE Table_type = 'VIEW';

-- Ver estrutura de uma tabela
DESCRIBE produtos;

-- Ver todos os produtos com categoria
SELECT * FROM vw_produtos_completos;

-- Ver todos os triggers
SHOW TRIGGERS;

-- Ver contagem de registros
SELECT 
    'usuarios' as tabela, COUNT(*) as total FROM usuarios
UNION ALL
SELECT 'produtos', COUNT(*) FROM produtos
UNION ALL
SELECT 'categorias', COUNT(*) FROM categorias;
```

## 🔍 Troubleshooting

### Container não inicia

```bash
# Verificar se a porta 13306 está em uso
sudo lsof -i :13306

# Remover volumes antigos se necessário
docker-compose down -v
docker-compose up -d
```

### Erro de conexão

```bash
# Verificar se o container está rodando
docker ps | grep mariadb

# Verificar logs do container
docker-compose logs mariadb_scee

# Testar conexão manualmente
docker exec -it mariadb_scee mysql -uscee_user -pscee_pass -e "SELECT 1"
```

### Erro ao executar schema.sql

```bash
# Garantir que FOREIGN_KEY_CHECKS está desabilitado
# O schema.sql já faz isso, mas se necessário:
docker exec -it mariadb_scee mysql -uscee_user -pscee_pass SCEE -e "SET FOREIGN_KEY_CHECKS = 0;"
```

## 📝 Diferenças SQLite → MySQL

### Tipos de Dados
- `INTEGER` → `INT`
- `TEXT` → `VARCHAR(n)` ou `TEXT`
- `REAL` → `DECIMAL(10, 2)` para valores monetários
- `BOOLEAN` → `BOOLEAN` (TINYINT(1) no MariaDB)
- `DATETIME` → `TIMESTAMP`

### Auto Increment
- `INTEGER PRIMARY KEY AUTOINCREMENT` → `INT AUTO_INCREMENT PRIMARY KEY`

### Constraints
- `CHECK(campo IN ('valor1', 'valor2'))` → `ENUM('valor1', 'valor2')`
- Índices criados inline na definição da tabela

### Timestamps Automáticos
- SQLite: Requer triggers
- MySQL: `ON UPDATE CURRENT_TIMESTAMP` nativo

### Triggers
- SQLite: `BEGIN ... END`
- MySQL: `DELIMITER $$` / `BEGIN ... END$$` / `DELIMITER ;`

### Inserts
- SQLite: `INSERT OR IGNORE`
- MySQL: `INSERT IGNORE`

## 🎯 Próximos Passos

1. ✅ Schema convertido para MySQL
2. ✅ Seed convertido para MySQL
3. ✅ Conexão configurada (pymysql)
4. ✅ Views criadas
5. ✅ Triggers implementados
6. ⏳ Atualizar repositories para usar pymysql (próximo passo)
7. ⏳ Testar CRUD operations
8. ⏳ Implementar API FastAPI
9. ⏳ Testes de integração

## 📚 Referências

- [MariaDB Documentation](https://mariadb.com/kb/en/)
- [PyMySQL Documentation](https://pymysql.readthedocs.io/)
- [FastAPI + MySQL](https://fastapi.tiangolo.com/tutorial/sql-databases/)
- [Docker Compose](https://docs.docker.com/compose/)
