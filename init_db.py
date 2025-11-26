#!/usr/bin/env python3
"""Script para inicializar o banco de dados do projeto SCEE.

Este script:
1. Cria o banco de dados SQLite
2. Executa o schema (cria todas as tabelas)
3. Opcionalmente popula com dados de seed

Usage:
    python init_db.py              # Apenas cria schema
    python init_db.py --seed       # Cria schema e popula com dados
    python init_db.py --reset      # Apaga tudo e recria (CUIDADO!)
"""
import sys
import argparse
import logging
from pathlib import Path

# Adiciona o diretório raiz ao path para imports
sys.path.insert(0, str(Path(__file__).parent))

from config.database import init_db, reset_db, check_connection, get_connection

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_seed_data():
    """Carrega dados de seed no banco de dados."""
    seed_path = Path(__file__).parent / 'seed' / 'seed.sql'
    
    if not seed_path.exists():
        logger.warning(f"Arquivo de seed não encontrado: {seed_path}")
        return
    
    logger.info("Carregando dados de seed...")
    
    try:
        with get_connection() as conn:
            with open(seed_path, 'r', encoding='utf-8') as f:
                seed_sql = f.read()
                conn.executescript(seed_sql)
            conn.commit()
        
        logger.info("✅ Dados de seed carregados com sucesso!")
    except Exception as e:
        logger.error(f"❌ Erro ao carregar dados de seed: {e}")
        raise


def main():
    """Função principal do script."""
    parser = argparse.ArgumentParser(
        description='Inicializa o banco de dados do projeto SCEE'
    )
    parser.add_argument(
        '--seed',
        action='store_true',
        help='Carregar dados de seed após criar schema'
    )
    parser.add_argument(
        '--reset',
        action='store_true',
        help='ATENÇÃO: Apaga o banco existente e recria do zero'
    )
    
    args = parser.parse_args()
    
    try:
        if args.reset:
            logger.warning("⚠️  ATENÇÃO: Resetando banco de dados (todos os dados serão perdidos)!")
            resposta = input("Tem certeza? Digite 'SIM' para confirmar: ")
            if resposta != 'SIM':
                logger.info("Operação cancelada.")
                return
            
            reset_db()
            logger.info("✅ Banco de dados resetado!")
        else:
            logger.info("Inicializando banco de dados...")
            init_db()
            logger.info("✅ Schema criado com sucesso!")
        
        if args.seed:
            load_seed_data()
        
        # Verifica conexão
        if check_connection():
            logger.info("✅ Conexão com banco de dados OK!")
            
            # Mostra estatísticas
            with get_connection() as conn:
                cursor = conn.execute("SELECT COUNT(*) as total FROM categorias")
                total_categorias = cursor.fetchone()['total']
                
                cursor = conn.execute("SELECT COUNT(*) as total FROM produtos")
                total_produtos = cursor.fetchone()['total']
                
                cursor = conn.execute("SELECT COUNT(*) as total FROM usuarios")
                total_usuarios = cursor.fetchone()['total']
                
                logger.info(f"📊 Estatísticas do banco:")
                logger.info(f"   - Categorias: {total_categorias}")
                logger.info(f"   - Produtos: {total_produtos}")
                logger.info(f"   - Usuários: {total_usuarios}")
        
        logger.info("\n🎉 Banco de dados pronto para uso!")
        logger.info("\nPróximos passos:")
        logger.info("1. Instalar dependências: pip install -r requirements.txt")
        logger.info("2. Iniciar API: uvicorn api.main:app --reload")
        
    except Exception as e:
        logger.error(f"❌ Erro: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
