#!/bin/bash
# Script de execução do SCEE
# ./run.sh

set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║              🚀 Iniciando SCEE                                 ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Verificar se ambiente virtual existe
if [ ! -d ".venv" ]; then
    echo "⚠️  Ambiente virtual não encontrado. Criando..."
    python3 -m venv .venv
    echo "✅ Ambiente virtual criado!"
fi

# Ativar ambiente virtual
echo "🔄 Ativando ambiente virtual..."
source .venv/bin/activate

# Verificar dependências
if ! python -c "import pymysql" 2>/dev/null; then
    echo "⚠️  Dependências não instaladas. Instalando..."
    pip install -q -r requirements.txt
    echo "✅ Dependências instaladas!"
fi

# Verificar Docker
echo "🐳 Verificando Docker..."
if ! docker compose ps | grep -q "scee_mariadb.*healthy"; then
    echo "⚠️  Banco de dados não está rodando. Iniciando..."
    docker compose up -d
    echo "⏳ Aguardando banco inicializar..."
    sleep 10
    python init_db.py --wait
fi

echo "✅ Docker OK!"
echo ""

# Executar aplicação
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║              🎯 Executando Aplicação SCEE                      ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "🔐 Credenciais:"
echo "   Admin: admin@scee.com / admin123"
echo "   Cliente: cliente@exemplo.com / cliente123"
echo ""

python main.py
