import sys
import os

# 1. Garante que o Python encontre a pasta 'src'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.models.users.admin_model import Administrador
from src.repositories.user_repository import UsuarioRepository
from src.utils.security.password_hasher import PasswordHasher
from src.config.database import DatabaseConnection

def criar_tabelas_e_admin():
    print("--- Iniciando Configuração do Banco de Dados ---")
    
    # 2. Força a criação das tabelas (Lendo o script SQL)
    try:
        db = DatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Lê o arquivo SQL que cria as tabelas
        # Certifique-se que a pasta 'schema' e o arquivo 'init_db.sql' existem!
        # Se não tiver o arquivo SQL, vamos criar as tabelas via código aqui mesmo por segurança:
        
        sql_create_users = """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha_hash TEXT NOT NULL,
            cpf TEXT,
            nivel_acesso TEXT,
            tipo TEXT NOT NULL,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(sql_create_users)
        conn.commit()
        print("Tabelas verificadas/criadas com sucesso.")
        
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")
        return

    # 3. Cria o Usuário Admin
    repo = UsuarioRepository()
    
    # Verifica se já existe
    if repo.buscar_por_email("admin@scee.com"):
        print("⚠️  O usuário admin@scee.com já existe!")
    else:
        # Cria hash da senha
        senha_segura = PasswordHasher.hash_password("admin123")
        
        # Cria objeto Admin
        admin = Administrador(
            nome="Admin Sistema",
            email="admin@scee.com",
            senha_hash=senha_segura,
            nivel_acesso="gerente"
        )
        
        try:
            repo.salvar(admin)
            print("Usuário Admin criado com sucesso!")
            print("Email: admin@scee.com")
            print("Senha: admin123")
        except Exception as e:
            print(f"Erro ao salvar admin: {e}")

if __name__ == "__main__":
    criar_tabelas_e_admin()