# 🚀 Guia Rápido - SCEE

## Iniciar Projeto (Primeira Vez)

```bash
# 1. Clonar repositório
git clone https://github.com/daniele-senko/SCEE.git
cd SCEE

# 2. Criar ambiente virtual
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Executar aplicação
python main.py
```

**Nota:** O banco de dados SQLite será criado automaticamente na primeira execução com todos os dados iniciais!

## Uso Diário

```bash
# Ativar ambiente
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows

# Executar aplicação
python main.py
```

## Comandos Úteis

### Banco de Dados

```bash
# Visualizar banco SQLite
sqlite3 database_sqlite/scee_loja.db

# Listar tabelas
sqlite3 database_sqlite/scee_loja.db ".tables"

# Ver dados de uma tabela
sqlite3 database_sqlite/scee_loja.db "SELECT * FROM usuarios;"

# Resetar banco (APAGA TUDO!)
rm database_sqlite/scee_loja.db
python main.py  # Recria automaticamente
```

### Aplicação

```bash
# Executar aplicação
python main.py

# Executar testes
pytest tests/
```

## Credenciais

### Login na Aplicação

- **Admin**: `admin@scee.com` / `admin123`
- **Cliente**: `cliente@exemplo.com` / `cliente123`

### Adminer (http://localhost:8081)

- **Sistema**: MySQL
- **Servidor**: mariadb
- **Usuário**: scee_user
- **Senha**: scee_pass
- **Banco**: SCEE

### MySQL Direto

```bash
# Host: localhost
# Porta: 13306
# Usuário: scee_user
## Credenciais

### Login na Aplicação

## Problemas Comuns

### "Erro ao criar banco de dados"

```bash
# Verificar permissões da pasta
ls -la database_sqlite/

# Recriar pasta se necessário
mkdir -p database_sqlite
python main.py
```

### "Banco de dados está corrompido"

```bash
# Remover banco e recriar
rm database_sqlite/scee_loja.db
python main.py
```buntu / Debian
sudo apt-get install python3-tk
```

## Estrutura de Pastas

```
SCEE/
├── main.py              # Executar aplicação
├── init_db.py           # Verificar banco
├── compose.yaml         # Docker services
SCEE/
├── main.py              # Executar aplicação
├── requirements.txt     # Dependências
├── database_sqlite/     # Banco de dados SQLite
├── src/                 # Código-fonte
│   ├── config/         # Configurações e inicialização do banco
│   ├── models/         # Modelos de dados
│   ├── services/       # Lógica de negócio
│   └── utils/          # Utilitários
├── repositories/        # Acesso a dados
├── schema/              # Schema SQL
## Links Úteis

- **Documentação Completa**: [README.md](README.md)
- **Database Initializer**: [docs/DATABASE_INITIALIZER.md](docs/DATABASE_INITIALIZER.md)
- **Credenciais**: [docs/CREDENCIAIS.md](docs/CREDENCIAIS.md)
- **Estrutura**: [docs/ESTRUTURA.md](docs/ESTRUTURA.md)DME.md)
- **Estrutura**: [docs/ESTRUTURA.md](docs/ESTRUTURA.md)

---

💡 **Dica**: Adicione este arquivo aos favoritos para consulta rápida!
