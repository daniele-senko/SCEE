#!/usr/bin/env python3
"""Script para verificar o banco de dados do projeto SCEE.

⚠️ NOTA: O Docker Compose já inicializa o banco automaticamente!

Para uso normal:
    docker compose up -d

Para verificar o banco:
    python init_db.py
"""
import sys
import time
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from config.database import check_connection, get_connection

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def wait_for_db(max_attempts=30):
    """Aguarda o banco de dados estar disponível."""
    logger.info("🔄 Aguardando banco de dados...")
    
    for attempt in range(1, max_attempts + 1):
        try:
            if check_connection():
                logger.info("✅ Banco disponível!")
                return True
        except:
            if attempt < max_attempts:
                logger.info(f"⏳ Tentativa {attempt}/{max_attempts}...")
                time.sleep(2)
    
    return False


def show_stats():
    """Mostra estatísticas."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            logger.info(f"📊 MySQL: {version[0]}")
            
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            logger.info(f"📋 Tabelas: {len(tables)}")
            
            stats = {}
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
                stats[table[0]] = cursor.fetchone()[0]
            
            logger.info("\n📊 Dados:")
            for table, count in sorted(stats.items()):
                if count > 0:
                    logger.info(f"   ✓ {table}: {count}")
            
            cursor.close()
    except Exception as e:
        logger.error(f"❌ Erro: {e}")


def main():
    """Função principal."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Verifica banco SCEE')
    parser.add_argument('--wait', action='store_true', help='Aguardar banco')
    args = parser.parse_args()
    
    try:
        logger.info("═" * 50)
        logger.info("  SCEE - Banco de Dados")
        logger.info("═" * 50 + "\n")
        
        if args.wait:
            if not wait_for_db():
                sys.exit(1)
        
        logger.info("🔍 Verificando conexão...")
        if not check_connection():
            logger.error("❌ Sem conexão!")
            logger.info("\n💡 Execute: docker compose up -d")
            sys.exit(1)
        
        logger.info("✅ Conectado!\n")
        show_stats()
        
        logger.info("\n" + "═" * 50)
        logger.info("🎉 Banco pronto!")
        logger.info("═" * 50)
        logger.info("\n📝 Próximos passos:")
        logger.info("   • python main.py")
        logger.info("   • http://localhost:8081 (Adminer)")
        
    except KeyboardInterrupt:
        logger.info("\n⚠️  Cancelado")
        sys.exit(0)
    except Exception as e:
        logger.error(f"\n❌ Erro: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
