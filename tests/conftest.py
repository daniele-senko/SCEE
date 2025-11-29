"""Configurações e fixtures compartilhadas para os testes."""
import pytest
import os
import sys
from pathlib import Path

# Adiciona o diretório raiz ao PYTHONPATH
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from src.config.database import DatabaseConnection
from src.config.database_initializer import DatabaseInitializer
from src.config.database_seeder import DatabaseSeeder


@pytest.fixture(scope="function")
def test_db_path(tmp_path):
    """Cria um banco de dados temporário para cada teste."""
    db_path = tmp_path / "test_scee.db"
    return str(db_path)


@pytest.fixture(scope="function")
def db_connection(test_db_path, monkeypatch):
    """Fornece uma conexão limpa com banco de dados de teste para cada teste."""
    # Fecha conexão anterior se existir
    if DatabaseConnection._instance is not None:
        if hasattr(DatabaseConnection._instance, '_conn') and DatabaseConnection._instance._conn:
            DatabaseConnection._instance._conn.close()
        # Força resetar a conexão interna para None
        DatabaseConnection._instance._conn = None
    
    # Reseta o singleton DatabaseConnection
    DatabaseConnection._instance = None
    
    # Faz monkeypatch DIRETO no Config.DB_PATH (não apenas na variável de ambiente)
    from src.config.settings import Config
    monkeypatch.setattr(Config, 'DB_PATH', test_db_path)
    
    # Remove o banco se existir
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
    
    # Inicializa o banco
    initializer = DatabaseInitializer()
    initializer.initialize_database()
    
    # Semeia dados de teste
    seeder = DatabaseSeeder()
    seeder.seed_all()
    
    # Retorna conexão
    conn = DatabaseConnection()
    
    yield conn
    
    # Cleanup - Fecha conexão e reseta singleton
    if conn._conn:
        conn._conn.close()
    conn._conn = None
    DatabaseConnection._instance = None
    if os.path.exists(test_db_path):
        os.remove(test_db_path)


@pytest.fixture
def sample_admin():
    """Retorna dados de exemplo de um administrador."""
    return {
        "email": "admin@scee.com",
        "senha": "admin123",
        "nome": "Administrador",
        "nivel_acesso": "gerente"
    }


@pytest.fixture
def sample_client():
    """Retorna dados de exemplo de um cliente."""
    return {
        "email": "joao@email.com",
        "senha": "cliente123",
        "nome": "João Silva",
        "cpf": "123.456.789-00"
    }


@pytest.fixture
def sample_product():
    """Retorna dados de exemplo de um produto."""
    return {
        "nome": "Produto Teste",
        "descricao": "Descrição do produto teste",
        "preco": 99.90,
        "sku": "TEST-001",
        "categoria_id": 1,
        "estoque": 10,
        "ativo": 1
    }
