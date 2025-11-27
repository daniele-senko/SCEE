import sqlite3
import os
from src.config.settings import Config

print(f"--- DEBUG BANCO DE DADOS ---")
print(f"Caminho esperado: {Config.DB_PATH}")

if not os.path.exists(Config.DB_PATH):
    print("❌ ERRO GRAVE: O arquivo do banco de dados NÃO EXISTE nesse caminho!")
else:
    print("✅ Arquivo do banco encontrado.")
    
    try:
        conn = sqlite3.connect(Config.DB_PATH)
        cursor = conn.cursor()
        
        # Tenta ler categorias
        cursor.execute("SELECT * FROM categorias")
        cats = cursor.fetchall()
        
        if not cats:
            print("❌ A tabela 'categorias' existe, mas está VAZIA.")
        else:
            print(f"✅ Encontradas {len(cats)} categorias:")
            for c in cats:
                # Acessa por índice pois row_factory pode não estar configurado aqui
                print(f"   - ID: {c[0]} | Nome: {c[1]}")
                
        conn.close()
    except Exception as e:
        print(f"❌ Erro ao ler banco: {e}")