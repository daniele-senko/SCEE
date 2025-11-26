# 🚀 Guia Rápido - SCEE

## Iniciar Projeto (Primeira Vez)

```bash
# 1. Clonar repositório
git clone https://github.com/daniele-senko/SCEE.git
cd SCEE

# 2. Criar ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Iniciar banco de dados (Docker)
docker compose up -d

# 5. Aguardar banco inicializar (30s) e verificar
sleep 30
python init_db.py --wait

# 6. Executar aplicação
python main.py
```

## Uso Diário

```bash
# Ativar ambiente
source .venv/bin/activate

# Iniciar serviços (se não estiverem rodando)
docker compose up -d

# Executar aplicação
python main.py
```

## Comandos Úteis

### Docker

```bash
# Iniciar serviços
docker compose up -d

# Parar serviços
docker compose down

# Ver logs do banco
docker compose logs -f mariadb

# Resetar banco (APAGA TUDO!)
docker compose down -v
docker compose up -d

# Status dos containers
docker compose ps
```

### Banco de Dados

```bash
# Verificar conexão
python init_db.py

# Aguardar banco estar pronto
python init_db.py --wait

# Acessar MySQL CLI
docker exec -it scee_mariadb mysql -uscee_user -pscee_pass SCEE

# Adminer (interface web)
# http://localhost:8081
```

### Aplicação

```bash
# Executar aplicação
python main.py

# Executar testes
python tests/test_connection.py
python tests/test_integration_mysql.py
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
# Senha: scee_pass
# Banco: SCEE
```

## Problemas Comuns

### "Erro ao conectar ao banco"

```bash
# Verificar se Docker está rodando
docker compose ps

# Reiniciar serviços
docker compose restart

# Ver logs para erros
docker compose logs mariadb
```

### "Porta 13306 já em uso"

```bash
# Alterar porta no compose.yaml
# Linha: - 13306:3306
# Para:  - 13307:3306

# Também atualizar config/database.py e .env
```

### "ModuleNotFoundError"

```bash
# Ativar ambiente virtual
source .venv/bin/activate

# Reinstalar dependências
pip install -r requirements.txt
```

### "Tkinter não encontrado"

```bash
# Rocky Linux / RHEL
sudo dnf install python3-tkinter

# Ubuntu / Debian
sudo apt-get install python3-tk
```

## Estrutura de Pastas

```
SCEE/
├── main.py              # Executar aplicação
├── init_db.py           # Verificar banco
├── compose.yaml         # Docker services
├── requirements.txt     # Dependências
├── gui/                 # Interface Tkinter
├── src/                 # Código-fonte
├── repositories/        # Acesso a dados
├── config/              # Configurações
├── schema/              # SQL schema
├── seed/                # Dados iniciais
├── tests/               # Testes
└── docs/                # Documentação
```

## Links Úteis

- **Documentação Completa**: [README.md](README.md)
- **Guia Tkinter**: [docs/TKINTER_README.md](docs/TKINTER_README.md)
- **Guia MySQL**: [docs/MYSQL_README.md](docs/MYSQL_README.md)
- **Estrutura**: [docs/ESTRUTURA.md](docs/ESTRUTURA.md)

---

💡 **Dica**: Adicione este arquivo aos favoritos para consulta rápida!
