#!/usr/bin/env python3
"""
Script para testar a conexão com o MySQL e executar o schema
"""
import os
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

from config.database import get_connection, init_db, reset_db


def test_connection():
    """Testa a conexão com o banco de dados MySQL"""
    print("🔍 Testando conexão com MySQL...")
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        
        print(f"✅ Conexão estabelecida com sucesso!")
        print(f"📊 Versão do MySQL: {version['VERSION()']}")
        
        cursor.execute("SELECT DATABASE()")
        db_name = cursor.fetchone()
        print(f"💾 Banco de dados atual: {db_name['DATABASE()']}")
        
        cursor.close()
        conn.close()
        
        return True
    except Exception as e:
        print(f"❌ Erro ao conectar com MySQL: {e}")
        return False


def show_tables():
    """Lista todas as tabelas do banco"""
    print("\n📋 Listando tabelas...")
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        if tables:
            print(f"\n✅ Total de tabelas: {len(tables)}")
            for table in tables:
                table_name = list(table.values())[0]
                print(f"  - {table_name}")
        else:
            print("⚠️  Nenhuma tabela encontrada")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ Erro ao listar tabelas: {e}")


def show_views():
    """Lista todas as views do banco"""
    print("\n👁️  Listando views...")
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SHOW FULL TABLES WHERE Table_type = 'VIEW'")
        views = cursor.fetchall()
        
        if views:
            print(f"\n✅ Total de views: {len(views)}")
            for view in views:
                view_name = list(view.values())[0]
                print(f"  - {view_name}")
        else:
            print("⚠️  Nenhuma view encontrada")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ Erro ao listar views: {e}")


def count_records(table_name):
    """Conta registros em uma tabela"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) as total FROM {table_name}")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result['total']
    except Exception as e:
        print(f"❌ Erro ao contar registros de {table_name}: {e}")
        return 0


def main():
    """Função principal"""
    print("=" * 60)
    print("🧪 TESTE DE CONEXÃO E SCHEMA MYSQL - SCEE")
    print("=" * 60)
    
    # Testa conexão
    if not test_connection():
        print("\n❌ Falha na conexão. Verifique se o MariaDB está rodando:")
        print("   docker-compose up -d")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("Opções:")
    print("1 - Listar tabelas e views")
    print("2 - Criar schema (init_db)")
    print("3 - Resetar banco (reset_db + init_db)")
    print("4 - Mostrar contagem de registros")
    print("0 - Sair")
    print("=" * 60)
    
    opcao = input("\nEscolha uma opção: ").strip()
    
    if opcao == "1":
        show_tables()
        show_views()
    
    elif opcao == "2":
        print("\n🔨 Executando init_db...")
        try:
            init_db()
            print("✅ Schema criado com sucesso!")
            show_tables()
            show_views()
        except Exception as e:
            print(f"❌ Erro ao criar schema: {e}")
    
    elif opcao == "3":
        confirmacao = input("\n⚠️  ATENÇÃO: Isso apagará todos os dados! Confirma? (sim/não): ")
        if confirmacao.lower() == "sim":
            print("\n🗑️  Resetando banco...")
            try:
                reset_db()
                print("✅ Banco resetado!")
                print("\n🔨 Criando schema novamente...")
                init_db()
                print("✅ Schema criado com sucesso!")
                show_tables()
                show_views()
            except Exception as e:
                print(f"❌ Erro: {e}")
        else:
            print("❌ Operação cancelada")
    
    elif opcao == "4":
        show_tables()
        print("\n📊 Contagem de registros:")
        tables = ['usuarios', 'clientes_info', 'administradores', 'categorias', 
                 'produtos', 'carrinhos', 'pedidos']
        for table in tables:
            count = count_records(table)
            print(f"  {table}: {count} registros")
    
    elif opcao == "0":
        print("\n👋 Até logo!")
    
    else:
        print("\n❌ Opção inválida!")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
