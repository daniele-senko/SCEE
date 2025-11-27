import sys
import os
import sqlite3

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.config.settings import Config

def criar_tabelas():
    print(f"--- 🛠️ Criando Tabelas (Com Proteção de Duplicidade) ---")
    
    os.makedirs(os.path.dirname(Config.DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(Config.DB_PATH)
    cursor = conn.cursor()
    
    # 1. Usuários
    cursor.execute("""
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
    """)
    
    # 2. Categorias (ADICIONADO 'UNIQUE' NO NOME)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE, 
        descricao TEXT,
        ativo INTEGER DEFAULT 1
    );
    """)
    
    # 3. Produtos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        descricao TEXT,
        sku TEXT UNIQUE NOT NULL,
        preco REAL NOT NULL,
        estoque INTEGER NOT NULL DEFAULT 0,
        categoria_id INTEGER,
        ativo INTEGER DEFAULT 1,
        FOREIGN KEY (categoria_id) REFERENCES categorias(id)
    );
    """)
    
    conn.commit()
    conn.close()
    print("✅ Tabelas recriadas com sucesso!")

if __name__ == "__main__":
    criar_tabelas()