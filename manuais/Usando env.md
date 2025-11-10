## Criar o Ambiente Virtual

No terminal, navegue até o diretório do projeto e execute o comando abaixo para criar o ambiente virtual:

```python -m venv venv```

No Linux ou macOS, você pode usar o seguinte comando:

```python3 -m venv venv```

Sair do Ambiente Virtual
Para sair do ambiente virtual, basta digitar o comando:

```deactivate```

## Instalar Dependências

Com o ambiente ativado, instale pacotes específicos usando o pip:

```pip install nome_do_pacote```


Por exemplo:

```pip install flask```

## Gerenciar Dependências com requirements.txt

Para salvar as dependências instaladas no ambiente virtual em um arquivo, execute:

```pip freeze > requirements.txt```

## Outros desenvolvedores podem instalar as mesmas dependências com:

```pip install -r requirements.txt```
