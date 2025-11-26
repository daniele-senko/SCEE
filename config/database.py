"""Configuração de conexão com banco de dados SQLite.

Este módulo fornece funções para gerenciar a conexão com o banco de dados
SQLite e inicializar o schema.
"""
import sqlite3
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# Caminho do banco de dados
DB_PATH = Path(__file__).resolve().parents[1] / 'data' / 'scee.db'
SCHEMA_PATH = Path(__file__).resolve().parents[1] / 'schema' / 'schema.sql'


def get_connection() -> sqlite3.Connection:
    """Obtém uma conexão com o banco de dados SQLite.
    
    Returns:
        sqlite3.Connection: Conexão ativa com o banco de dados.
    """
    # Garante que o diretório data existe
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row  # Permite acessar colunas por nome
    
    # Habilita foreign keys (importante no SQLite)
    conn.execute("PRAGMA foreign_keys = ON")
    
    return conn


def init_db(schema_path: Optional[Path] = None) -> None:
    """Inicializa o banco de dados executando o schema SQL.
    
    Args:
        schema_path: Caminho opcional para o arquivo de schema.
                    Se não fornecido, usa o schema padrão.
    """
    if schema_path is None:
        schema_path = SCHEMA_PATH
    
    if not schema_path.exists():
        raise FileNotFoundError(f"Arquivo de schema não encontrado: {schema_path}")
    
    logger.info(f"Inicializando banco de dados com schema: {schema_path}")
    
    with get_connection() as conn:
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
            conn.executescript(schema_sql)
        conn.commit()
    
    logger.info("Banco de dados inicializado com sucesso!")


def reset_db() -> None:
    """Remove o banco de dados existente e recria do zero.
    
    ATENÇÃO: Esta função apaga TODOS os dados do banco!
    Use apenas em desenvolvimento/testes.
    """
    if DB_PATH.exists():
        logger.warning(f"Removendo banco de dados existente: {DB_PATH}")
        DB_PATH.unlink()
    
    init_db()
    logger.info("Banco de dados resetado com sucesso!")


def check_connection() -> bool:
    """Verifica se é possível conectar ao banco de dados.
    
    Returns:
        bool: True se a conexão foi bem-sucedida, False caso contrário.
    """
    try:
        with get_connection() as conn:
            cursor = conn.execute("SELECT 1")
            cursor.fetchone()
        return True
    except Exception as e:
        logger.error(f"Erro ao conectar ao banco de dados: {e}")
        return False


if __name__ == "__main__":
    # Permite executar este arquivo diretamente para inicializar o banco
    logging.basicConfig(level=logging.INFO)
    init_db()
    print(f"✅ Banco de dados criado em: {DB_PATH}")
