# 📦 Instalação de Dependências - SCEE

## 🚀 Instalação Rápida

### Produção

```bash
# Instalar dependências de produção
pip install -r requirements.txt
```

### Desenvolvimento

```bash
# Instalar dependências de desenvolvimento (inclui testes, linters, etc)
pip install -r requirements-dev.txt
```

---

## 📋 Dependências por Categoria

### 🗄️ Database
- **pymysql** (1.1.0) - Driver MySQL/MariaDB
- **cryptography** (41.0.7) - Criptografia para conexões
- **sqlalchemy** (2.0.23) - ORM (opcional)

### 🔐 Segurança
- **passlib[bcrypt]** (1.7.4) - Hash de senhas
- **bcrypt** (4.1.1) - Algoritmo de hash
- **email-validator** (2.1.0) - Validação de emails

### 🎨 GUI
- **Pillow** (10.1.0) - Manipulação de imagens
- **tkinter** - Interface gráfica (já incluído no Python)

### 🧪 Testes
- **pytest** (7.4.3) - Framework de testes
- **pytest-cov** (4.1.0) - Cobertura de código
- **pytest-mock** (3.12.0) - Mocks para testes
- **coverage** (7.3.2) - Análise de cobertura

### 🛠️ Desenvolvimento
- **black** (23.12.1) - Formatador de código
- **pylint** (3.0.3) - Linter
- **mypy** (1.7.1) - Type checker
- **ipython** (8.18.1) - REPL interativo
- **jupyter** (1.0.0) - Notebooks

---

## 🔧 Instalação por Ambiente

### Ambiente Virtual (Recomendado)

```bash
# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual
# Linux/Mac:
source .venv/bin/activate

# Windows:
.venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Para desenvolvimento:
pip install -r requirements-dev.txt
```

### Sistema Global

```bash
# Não recomendado, mas funciona
pip install -r requirements.txt
```

### Docker (Futuro)

```bash
# Construir imagem
docker build -t scee:latest .

# Executar container
docker run -it scee:latest
```

---

## ✅ Verificar Instalação

```bash
# Verificar versões instaladas
pip list

# Verificar dependências
pip check

# Executar testes para validar
pytest tests/ -v
```

---

## 🔄 Atualizar Dependências

```bash
# Atualizar todas as dependências
pip install --upgrade -r requirements.txt

# Atualizar pacote específico
pip install --upgrade pytest

# Gerar arquivo de versões atuais
pip freeze > requirements-lock.txt
```

---

## 📊 Dependências Instaladas

### Produção (requirements.txt)
```
pymysql==1.1.0
cryptography==41.0.7
sqlalchemy==2.0.23
passlib[bcrypt]==1.7.4
bcrypt==4.1.1
email-validator==2.1.0
Pillow==10.1.0
python-dotenv==1.0.0
pytest==7.4.3
pytest-cov==4.1.0
pytest-mock==3.12.0
coverage==7.3.2
pytest-asyncio==0.21.1
```

### Desenvolvimento (requirements-dev.txt)
Inclui todas de produção +
```
pytest-xdist==3.5.0
pytest-watch==4.2.0
pylint==3.0.3
flake8==6.1.0
black==23.12.1
isort==5.13.2
mypy==1.7.1
bandit==1.7.5
sphinx==7.2.6
ipython==8.18.1
jupyter==1.0.0
faker==21.0.0
rich==13.7.0
+ mais...
```

---

## 🐛 Problemas Comuns

### ImportError ao executar testes

```bash
# Solução: Instalar dependências de teste
pip install pytest pytest-mock pytest-cov
```

### ModuleNotFoundError: No module named 'passlib'

```bash
# Solução: Instalar passlib com bcrypt
pip install 'passlib[bcrypt]'
```

### Erro de criptografia no MySQL

```bash
# Solução: Instalar cryptography
pip install cryptography
```

### Pillow não instala (erro de compilação)

```bash
# Linux: Instalar dependências do sistema
sudo apt-get install libjpeg-dev zlib1g-dev

# Mac:
brew install libjpeg

# Depois reinstalar
pip install Pillow
```

---

## 🎯 Comandos Úteis

```bash
# Listar dependências instaladas
pip list

# Verificar dependências quebradas
pip check

# Mostrar informações de um pacote
pip show pytest

# Desinstalar pacote
pip uninstall pytest

# Instalar versão específica
pip install pytest==7.4.3

# Instalar em modo editable (desenvolvimento)
pip install -e .
```

---

## 📚 Documentação das Dependências

- **PyMySQL**: https://pymysql.readthedocs.io/
- **Pytest**: https://docs.pytest.org/
- **Passlib**: https://passlib.readthedocs.io/
- **Pillow**: https://pillow.readthedocs.io/
- **Black**: https://black.readthedocs.io/

---

## 🔐 Segurança

```bash
# Verificar vulnerabilidades (requer safety)
pip install safety
safety check

# Escanear código (requer bandit)
pip install bandit
bandit -r src/
```

---

## 💡 Dicas

1. **Sempre use ambiente virtual** - Evita conflitos de dependências
2. **Mantenha requirements.txt atualizado** - Documente novas dependências
3. **Use pip freeze com cuidado** - Pode incluir dependências transitivas
4. **Teste após atualizar** - Execute `pytest` após atualizar pacotes
5. **Versione requirements-lock.txt** - Para reproduzir ambiente exato

---

## 🆘 Suporte

Se encontrar problemas:
1. Verifique a versão do Python: `python --version` (requer 3.9+)
2. Atualize pip: `pip install --upgrade pip`
3. Limpe cache: `pip cache purge`
4. Reinstale do zero: Delete `.venv` e recrie

---

✅ **Pronto!** Todas as dependências necessárias para executar e desenvolver o SCEE.
