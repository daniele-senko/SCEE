import os
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env (se existir)
load_dotenv()

class Config:
    """
    Configurações globais do sistema.
    Classe Python pura, sem dependência do Pydantic.
    """
    
    # --- Caminhos e Sistema ---
    # Pega o diretório raiz do projeto dinamicamente
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Configuração do Banco
    DB_NAME = os.getenv("DB_NAME", "scee_loja.db")
    DB_PATH = os.path.join(BASE_DIR, "database_sqlite", DB_NAME)
    
    # --- Interface Gráfica (UI/Tkinter) ---
    APP_NAME = "SCEE - Eletrônicos"
    WINDOW_SIZE = "1024x768"
    
    # Paleta de Cores (Tema Escuro Profissional)
    COLOR_PRIMARY = "#2C3E50"      # Azul Petróleo (Menus)
    COLOR_SECONDARY = "#E74C3C"    # Vermelho (Ações/Alerta)
    COLOR_ACCENT = "#3498DB"       # Azul Claro (Destaques)
    COLOR_BG = "#ECF0F1"           # Fundo Cinza Claro
    COLOR_WHITE = "#FFFFFF"        # Branco
    COLOR_TEXT = "#2C3E50"         # Texto Escuro
    COLOR_TEXT_LIGHT = "#7F8C8D"   # Texto Secundário
    
    # Fontes Padrão (Tuplas para o Tkinter)
    # Usando TkDefaultFont para evitar erro X11 BadLength no Rocky Linux
    # TkDefaultFont é a fonte bitmap padrão do Tk, não usa RENDER extension
    FONT_TITLE = ("TkDefaultFont", 14, "bold")
    FONT_HEADER = ("TkDefaultFont", 12, "bold")
    FONT_BODY = ("TkDefaultFont", 10)
    FONT_SMALL = ("TkDefaultFont", 9)