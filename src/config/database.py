"""Configuração de conexão com banco de dados MySQL/MariaDB.

Este módulo fornece funções para gerenciar a conexão com o banco de dados
MySQL/MariaDB e inicializar o schema.
"""
import pymysql
from pathlib import Path
from typing import Optional
import logging
import os

logger = logging.getLogger(__name__)

# Configurações do banco de dados MySQL
DB_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'port': int(os.getenv('MYSQL_PORT', 13306)),
    'user': os.getenv('MYSQL_USER', 'scee_user'),
    'password': os.getenv('MYSQL_PASSWORD', 'scee_pass'),
    'database': os.getenv('MYSQL_DATABASE', 'SCEE'),
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
    'autocommit': False
}

SCHEMA_PATH = Path(__file__).resolve().parents[1] / 'schema' / 'schema.sql'


def get_connection() -> pymysql.Connection:
    """Obtém uma conexão com o banco de dados MySQL.
    
    Returns:
        pymysql.Connection: Conexão ativa com o banco de dados.
    """
    try:
        conn = pymysql.connect(**DB_CONFIG)
        return conn
    except pymysql.Error as e:
        logger.error(f"Erro ao conectar ao MySQL: {e}")
        raise


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
    
    logger.info(f"Inicializando banco de dados MySQL com schema: {schema_path}")
    
    try:
        with get_connection() as conn:
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema_sql = f.read()
                
            # Executar cada statement separadamente
            cursor = conn.cursor()
            
            # Dividir por ponto-e-vírgula e executar cada comando
            statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]
            
            for statement in statements:
                if statement:
                    try:
                        cursor.execute(statement)
                    except pymysql.Error as e:
                        # Ignorar erros de "tabela já existe"
                        if "already exists" not in str(e).lower():
                            logger.warning(f"Aviso ao executar statement: {e}")
            
            conn.commit()
            cursor.close()
        
        logger.info("Banco de dados inicializado com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao inicializar banco de dados: {e}")
        raise


def reset_db() -> None:
    """Remove todas as tabelas e recria do zero.
    
    ATENÇÃO: Esta função apaga TODOS os dados do banco!
    Use apenas em desenvolvimento/testes.
    """
    logger.warning("⚠️  Resetando banco de dados MySQL...")
    
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            
            # Desabilitar verificação de foreign keys temporariamente
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            
            # Buscar todas as tabelas
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            # Dropar cada tabela
            for table in tables:
                table_name = list(table.values())[0]
                logger.info(f"Dropando tabela: {table_name}")
                cursor.execute(f"DROP TABLE IF EXISTS `{table_name}`")
            
            # Reabilitar verificação de foreign keys
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            
            conn.commit()
            cursor.close()
        
        logger.info("✅ Tabelas removidas com sucesso!")
        
        # Recriar schema
        init_db()
        logger.info("✅ Banco de dados resetado!")
        
    except Exception as e:
        logger.error(f"Erro ao resetar banco de dados: {e}")
        raise


def check_connection() -> bool:
    """Verifica se é possível conectar ao banco de dados.
    
    Returns:
        bool: True se a conexão foi bem-sucedida, False caso contrário.
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            cursor.close()
        return True
    except Exception as e:
        logger.error(f"Erro ao conectar ao banco de dados: {e}")
        return False


if __name__ == "__main__":
    # Permite executar este arquivo diretamente para inicializar o banco
    logging.basicConfig(level=logging.INFO)
    init_db()
    print(f"✅ Banco de dados MySQL inicializado!")

