from config.database import DatabaseConfig

def create_usuarios_table():
    """Cria a tabela de usuários no banco SCEE"""
    db_config = DatabaseConfig()
    conn = db_config.connect()

    if conn:
        cursor = conn.cursor()

        create_table_query = """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            full_name VARCHAR(100) NOT NULL,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """

        try:
            cursor.execute(create_table_query)
            conn.commit()
            print("Tabela 'usuarios' criada com sucesso!")
        except Exception as e:
            print(f"Erro ao criar tabela: {e}")
        finally:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    create_usuarios_table()