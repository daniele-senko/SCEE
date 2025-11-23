import os
from dotenv import load_dotenv

load_dotenv()

DB_SETTINGS = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", 13306)),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

# configurações de interface (Tkinter)
APP_NAME = "SCEE - Sistema de Comércio Eletrônico"
WINDOW_SIZE = "1024x768"

# paleta de cores do tkinter
COLOR_PRIMARY = "#2C3E50"    # Azul Escuro
COLOR_SECONDARY = "#E74C3C"  # Vermelho Alerta
COLOR_BACKGROUND = "#ECF0F1" # Cinza Claro
COLOR_TEXT = "#2C3E50"