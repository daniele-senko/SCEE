@echo off
REM Script de execução do SCEE para Windows
REM run.bat

echo ========================================================
echo              INICIANDO SCEE
echo ========================================================
echo.

REM Verificar se ambiente virtual existe
if not exist ".venv\" (
    echo Ambiente virtual nao encontrado. Criando...
    python -m venv .venv
    echo Ambiente virtual criado!
)

REM Ativar ambiente virtual
echo Ativando ambiente virtual...
call .venv\Scripts\activate.bat

REM Verificar dependências
python -c "import pymysql" 2>nul
if errorlevel 1 (
    echo Dependencias nao instaladas. Instalando...
    pip install -q -r requirements.txt
    echo Dependencias instaladas!
)

REM Verificar Docker
echo Verificando Docker...
docker compose ps | findstr "scee_mariadb.*healthy" >nul 2>&1
if errorlevel 1 (
    echo Banco de dados nao esta rodando. Iniciando...
    docker compose up -d
    echo Aguardando banco inicializar...
    timeout /t 10 /nobreak >nul
    python init_db.py --wait
)

echo Docker OK!
echo.

REM Executar aplicação
echo ========================================================
echo              EXECUTANDO APLICACAO SCEE
echo ========================================================
echo.
echo Credenciais:
echo    Admin: admin@scee.com / admin123
echo    Cliente: cliente@exemplo.com / cliente123
echo.

python main.py

pause
