import sqlite3
import os
from src.config.settings import Config

class DatabaseConnection:
    """
    Gerenciador de conexão com banco de dados SQLite (Singleton).
    """
    
    _instance = None

    def __new__(cls):
        # Implementação do padrão Singleton para garantir uma única instância
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance._conn = None
        return cls._instance

    def get_connection(self):
        """
        Retorna a conexão ativa com o banco de dados.
        Cria uma nova se não existir.
        """
        if self._conn is None:
            # Garante que a pasta 'data' existe antes de conectar
            os.makedirs(os.path.dirname(Config.DB_PATH), exist_ok=True)
            
            try:
                # Conecta ao arquivo definido no settings
                self._conn = sqlite3.connect(Config.DB_PATH)
                
                # Habilita o acesso às colunas pelo nome (ex: row['email'])
                self._conn.row_factory = sqlite3.Row
                
                # Habilita chaves estrangeiras (Foreign Keys) no SQLite
                self._conn.execute("PRAGMA foreign_keys = ON")
                
            except sqlite3.Error as e:
                print(f"Erro crítico ao conectar ao banco de dados: {e}")
                raise
                
        return self._conn

    def close_connection(self):
        """Fecha a conexão se estiver aberta."""
        if self._conn:
            self._conn.close()
            self._conn = None