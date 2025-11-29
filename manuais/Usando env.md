# Guia de Uso do Ambiente Virtual Python

## Criar o Ambiente Virtual

No terminal, navegue até o diretório do projeto e execute o comando abaixo para criar o ambiente virtual:

```bash
python -m venv .venv
```

No Linux ou macOS, você pode usar o seguinte comando:

```bash
python3 -m venv .venv
```

## Ativar o Ambiente Virtual

### Linux / macOS
```bash
source .venv/bin/activate
```

### Windows
```bash
.venv\Scripts\activate
```

Quando ativado, você verá `(.venv)` no início da linha do terminal.

## Sair do Ambiente Virtual

Para sair do ambiente virtual, basta digitar o comando:

```bash
deactivate
```

## Instalar Dependências

Com o ambiente ativado, instale pacotes específicos usando o pip:

```bash
pip install nome_do_pacote
```

Por exemplo:

```bash
pip install tkinter
```

## Gerenciar Dependências com requirements.txt

### Salvar Dependências

Para salvar as dependências instaladas no ambiente virtual em um arquivo, execute:

```bash
pip freeze > requirements.txt
```

### Instalar Dependências

Outros desenvolvedores podem instalar as mesmas dependências com:

```bash
pip install -r requirements.txt
```

## Projeto SCEE

Para este projeto especificamente:

```bash
# 1. Criar ambiente
python3 -m venv .venv

# 2. Ativar
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows

# 3. Instalar dependências do projeto
pip install -r requirements.txt

# 4. Executar aplicação
python main.py
```

O banco de dados SQLite será criado automaticamente na primeira execução!
