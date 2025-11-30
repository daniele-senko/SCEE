# 🚀 Guia Rápido - SCEE

## ⚡ Início Rápido (3 minutos)

```bash
# 1. Clonar e entrar no projeto
git clone https://github.com/daniele-senko/SCEE.git
cd SCEE

# 2. Criar ambiente virtual
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Executar aplicação
python main.py
```

✨ **Pronto!** O banco SQLite é criado automaticamente com dados de exemplo.

## 🔐 Credenciais de Acesso

| Tipo | Email | Senha |
|------|-------|-------|
| **Cliente** | `cliente@scee.com` | `cliente123` |
| **Admin** | `admin@scee.com` | `admin123` |

## 🎯 Uso Diário

```bash
# Ativar ambiente virtual
source .venv/bin/activate  # Linux/Mac

# Executar
python main.py
```

## 🛠️ Comandos Úteis

### Testes

```bash
# Executar todos os testes
pytest

# Com cobertura
pytest --cov=src --cov-report=html

# Modo verbose
pytest -v

# Parar no primeiro erro
pytest -x
```

### Banco de Dados SQLite

```bash
# Abrir banco no terminal
sqlite3 database_sqlite/scee_loja.db

# Listar todas as tabelas
sqlite3 database_sqlite/scee_loja.db ".tables"

# Ver estrutura de uma tabela
sqlite3 database_sqlite/scee_loja.db ".schema produtos"

# Consultar dados
sqlite3 database_sqlite/scee_loja.db "SELECT * FROM usuarios;"

# Exportar dados
sqlite3 database_sqlite/scee_loja.db ".dump" > backup.sql

# Resetar banco (⚠️ APAGA TUDO!)
rm database_sqlite/scee_loja.db
python main.py  # Recria com dados iniciais
```

### Git

```bash
# Ver status
git status

# Criar nova feature
git checkout -b feature/minha-feature

# Commit
git add .
git commit -m "feat: adiciona minha feature"

# Push
git push origin feature/minha-feature
```

## ⚠️ Problemas Comuns

### Erro: "ModuleNotFoundError: No module named 'tkinter'"

```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Rocky Linux/RHEL/Fedora
sudo dnf install python3-tkinter

# macOS
brew install python-tk@3.9
```

### Erro: "Permission denied" ao criar banco

```bash
# Verificar permissões
ls -la database_sqlite/

# Criar diretório se necessário
mkdir -p database_sqlite
chmod 755 database_sqlite

# Executar novamente
python main.py
```

### Banco de dados corrompido

```bash
# Fazer backup (opcional)
cp database_sqlite/scee_loja.db database_sqlite/scee_loja.db.bak

# Remover e recriar
rm database_sqlite/scee_loja.db
python main.py
```

### Erro X11 no Rocky Linux

Ver solução completa em: [`docs/ERRO_X11.md`](docs/ERRO_X11.md)

```bash
# Resumo: usar fontes bitmap
# O sistema já está configurado para evitar esse erro
```

### Ambiente virtual não ativa

```bash
# Certifique-se de estar no diretório correto
cd SCEE

# Recriar ambiente virtual
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 📁 Estrutura Simplificada

```
SCEE/
├── main.py                    # ← Executar aqui
├── requirements.txt           # Dependências
│
├── database_sqlite/          
│   └── scee_loja.db          # Banco (criado automaticamente)
│
├── src/
│   ├── views/                # Interface Tkinter
│   │   ├── client/          # Telas do cliente
│   │   └── admin/           # Telas do admin
│   │
│   ├── services/             # Lógica de negócio
│   ├── repositories/         # Acesso ao banco
│   ├── models/               # Entidades
│   └── config/               # Configurações
│
├── schema/                    # SQL do banco
├── seed/                      # Dados iniciais
├── tests/                     # 112 testes
└── docs/                      # Documentação
```

## 🎓 Fluxo de Trabalho

1. **Primeira vez**:
   ```bash
   git clone ... && cd SCEE
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   python main.py
   ```

2. **Desenvolvimento**:
   ```bash
   source .venv/bin/activate
   git checkout -b feature/minha-feature
   # ... fazer mudanças ...
   pytest  # testar
   python main.py  # executar
   git commit -m "feat: ..."
   git push
   ```

3. **Testes**:
   ```bash
   pytest -v  # todos os testes
   pytest tests/test_services/  # específico
   pytest --cov=src  # com cobertura
   ```

## 📚 Links Importantes

| Documento | Descrição |
|-----------|-----------|
| [README.md](README.md) | Documentação completa do projeto |
| [docs/INSTALACAO.md](docs/INSTALACAO.md) | Instalação detalhada (Rocky Linux) |
| [docs/UML.md](docs/UML.md) | Diagramas de arquitetura |
| [docs/ERRO_X11.md](docs/ERRO_X11.md) | Solução de problemas X11 |

## 💡 Dicas Rápidas

### Navegação no Sistema

**Área do Cliente:**
- Login → Home → Produtos → Carrinho → Checkout → Meus Pedidos

**Área Admin:**
- Login → Dashboard → Produtos/Categorias/Pedidos

### Dados de Teste

O banco vem com:
- ✅ 5 categorias (Eletrônicos, Roupas, Livros, Casa, Esportes)
- ✅ 15 produtos com estoque
- ✅ 2 usuários (admin + cliente)
- ✅ Endereços de exemplo

### Atalhos Úteis

```bash
# Alias úteis (adicione ao ~/.bashrc ou ~/.zshrc)
alias scee-run="cd ~/SCEE && source .venv/bin/activate && python main.py"
alias scee-test="cd ~/SCEE && source .venv/bin/activate && pytest -v"
alias scee-db="sqlite3 ~/SCEE/database_sqlite/scee_loja.db"
```

## 🆘 Precisa de Ajuda?

1. Consulte a [documentação completa](README.md)
2. Veja os [problemas comuns](#️-problemas-comuns) acima
3. Abra uma [issue no GitHub](https://github.com/daniele-senko/SCEE/issues)

---

<div align="center">

**🚀 Pronto para começar? Execute `python main.py`!**

*Última atualização: 29 de Novembro de 2025*

</div>
