from config.database import DatabaseConfig

def test_database_connection():
    """Testa a conexão com o banco de dados MySQL"""
    print("Tentando conectar ao banco de dados...")

    db_config = DatabaseConfig()
    conn = db_config.connect()

    if conn:
        print("✓ Conexão estabelecida com sucesso!")

        # Teste simples: verifica a versão do MySQL
        cursor = conn.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"✓ Versão do MySQL: {version[0]}")

        # Lista as tabelas do banco
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"✓ Tabelas encontradas: {len(tables)}")
        for table in tables:
            print(f"  - {table[0]}")

        cursor.close()
        conn.close()
        print("✓ Conexão fechada com sucesso!")
        return True
    else:
        print("✗ Falha ao conectar ao banco de dados")
        return False

if __name__ == "__main__":
    test_database_connection()