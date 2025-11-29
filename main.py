import sys
import os

# Adiciona o diretório raiz ao path do Python para garantir imports corretos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.views.main_window import MainWindow
from src.config.database import DatabaseConnection
from src.config.database_initializer import DatabaseInitializer

def main():
    """Função principal que inicia a aplicação."""
    try:
        # 1. Inicializa o banco de dados silenciosamente
        db = DatabaseConnection()
        initializer = DatabaseInitializer(db)
        
        # Verifica se o banco precisa ser criado
        if not initializer.check_database_exists():
            initializer.initialize_database()
        
        # 2. Inicia a Interface Gráfica
        app = MainWindow()
        app.mainloop()
        
    except Exception as e:
        print(f"Erro fatal ao iniciar a aplicação: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()