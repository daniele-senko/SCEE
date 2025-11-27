import sys
import os

# Adiciona o diretório raiz ao path do Python para garantir imports corretos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.views.main_window import MainWindow
# from src.config.database import DatabaseConnection (Podemos iniciar o banco aqui se quiser)

def main():
    """Função principal que inicia a aplicação."""
    try:
        # 1. Inicializa configurações ou Banco de Dados (se necessário pré-carregar)
        # db = DatabaseConnection()
        # db.get_connection()
        
        # 2. Inicia a Interface Gráfica
        app = MainWindow()
        app.mainloop()
        
    except Exception as e:
        print(f"Erro fatal ao iniciar a aplicação: {e}")

if __name__ == "__main__":
    main()