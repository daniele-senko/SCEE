# Guia de Testes do SCEE

## Configuração

1. **Ative o ambiente virtual:**
```bash
source venv/bin/activate
```

2. **Instale as dependências (se ainda não fez):**
```bash
pip install -r requirements.txt
```

## Executando os Testes

### Executar todos os testes
```bash
pytest
```

### Executar testes com saída detalhada
```bash
pytest -v
```

### Executar testes de um arquivo específico
```bash
pytest tests/services/test_auth_service.py
```

### Executar um teste específico
```bash
pytest tests/services/test_auth_service.py::TestAuthService::test_login_admin_sucesso
```

### Executar testes com cobertura
```bash
pytest --cov=src --cov-report=html
```

Após executar, abra `htmlcov/index.html` no navegador para ver o relatório detalhado.

### Executar testes com cobertura no terminal
```bash
pytest --cov=src --cov-report=term-missing
```

### Executar apenas testes rápidos (excluindo lentos)
```bash
pytest -m "not slow"
```

### Executar apenas testes de integração
```bash
pytest -m integration
```

### Executar testes e parar no primeiro erro
```bash
pytest -x
```

### Executar testes em modo verboso com traceback completo
```bash
pytest -vv --tb=long
```

## Estrutura de Testes

```
tests/
├── __init__.py
├── conftest.py              # Fixtures compartilhadas
├── services/               # Testes de serviços
│   ├── test_auth_service.py
│   ├── test_cart_service.py
│   └── ...
└── repositories/           # Testes de repositórios
    ├── test_user_repository.py
    ├── test_product_repository.py
    └── ...
```

## Fixtures Disponíveis

### `db_connection`
Fornece uma conexão limpa com banco de dados de teste (SQLite em memória).

**Uso:**
```python
def test_exemplo(db_connection):
    # Banco já está inicializado e populado com dados de teste
    repo = UsuarioRepository()
    usuario = repo.buscar_por_email("admin@scee.com")
    assert usuario is not None
```

### `sample_admin`
Retorna dados de exemplo de um administrador.

### `sample_client`
Retorna dados de exemplo de um cliente.

### `sample_product`
Retorna dados de exemplo de um produto.

## Escrevendo Novos Testes

### Exemplo de teste de serviço:
```python
def test_meu_servico(db_connection):
    """Descrição do que o teste faz."""
    # Arrange - Prepara dados
    servico = MeuServico()
    
    # Act - Executa ação
    resultado = servico.fazer_algo()
    
    # Assert - Verifica resultado
    assert resultado is not None
```

### Exemplo de teste com mock:
```python
from unittest.mock import Mock, patch

def test_com_mock(db_connection):
    """Teste usando mock."""
    with patch('src.services.email_service.EmailService.enviar') as mock_enviar:
        mock_enviar.return_value = True
        
        # Teste seu código aqui
        assert mock_enviar.called
```

## Boas Práticas

1. **Um teste, uma responsabilidade**: Cada teste deve verificar apenas uma coisa
2. **Nomes descritivos**: Use nomes que expliquem o que está sendo testado
3. **AAA Pattern**: Arrange, Act, Assert
4. **Isolamento**: Testes não devem depender uns dos outros
5. **Cleanup**: Use fixtures para garantir limpeza após testes
6. **Coverage**: Objetivo mínimo de 80% de cobertura

## Troubleshooting

### Erro: ModuleNotFoundError
Certifique-se de estar no diretório raiz do projeto e com venv ativado.

### Banco de dados travado
Os testes criam bancos temporários. Se houver problemas, delete os arquivos `.db` na pasta `tests/`.

### Testes lentos
Use `-n auto` para executar testes em paralelo (requer `pytest-xdist`):
```bash
pip install pytest-xdist
pytest -n auto
```
