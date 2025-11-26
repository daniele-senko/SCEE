#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCEE - Sistema de Comércio Eletrônico
Aplicação Desktop com Tkinter e MySQL
"""

import sys
import tkinter as tk
from tkinter import messagebox
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scee.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Importar views
from gui.views.login_view import LoginView
from gui.views.main_view import MainView


class SCEEApp:
    """Aplicação principal do SCEE"""
    
    def __init__(self):
        """Inicializa a aplicação"""
        self.root = tk.Tk()
        self.root.title("SCEE - Sistema de Comércio Eletrônico")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)
        
        # Centralizar janela
        self.center_window()
        
        # Configurar estilo
        self.configure_styles()
        
        # Usuário logado
        self.current_user = None
        
        # Mostrar tela de login
        self.show_login()
        
    def center_window(self):
        """Centraliza a janela na tela"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def configure_styles(self):
        """Configura estilos globais da aplicação"""
        self.root.configure(bg='#f0f0f0')
        
        # Definir cores padrão
        self.colors = {
            'primary': '#2563eb',      # Azul
            'secondary': '#64748b',    # Cinza
            'success': '#16a34a',      # Verde
            'danger': '#dc2626',       # Vermelho
            'warning': '#ea580c',      # Laranja
            'bg_light': '#f8fafc',     # Fundo claro
            'bg_dark': '#1e293b',      # Fundo escuro
            'text': '#1e293b',         # Texto escuro
            'text_light': '#64748b',   # Texto claro
        }
        
    def show_login(self):
        """Mostra a tela de login"""
        logger.info("Mostrando tela de login")
        
        # Limpar janela
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Criar view de login
        login_view = LoginView(self.root, self.on_login_success)
        
    def on_login_success(self, user_data):
        """Callback quando login é bem-sucedido"""
        logger.info(f"Login bem-sucedido: {user_data.get('email')}")
        self.current_user = user_data
        self.show_main_view()
        
    def show_main_view(self):
        """Mostra a tela principal"""
        logger.info("Mostrando tela principal")
        
        # Limpar janela
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Criar view principal
        main_view = MainView(self.root, self.current_user, self.on_logout)
        
    def on_logout(self):
        """Callback quando usuário faz logout"""
        logger.info("Logout realizado")
        self.current_user = None
        self.show_login()
        
    def run(self):
        """Inicia o loop principal da aplicação"""
        logger.info("Iniciando aplicação SCEE")
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            logger.info("Aplicação interrompida pelo usuário")
            self.quit()
        except Exception as e:
            logger.error(f"Erro na aplicação: {e}", exc_info=True)
            messagebox.showerror("Erro", f"Erro inesperado: {e}")
            self.quit()
            
    def quit(self):
        """Encerra a aplicação"""
        logger.info("Encerrando aplicação")
        self.root.quit()
        self.root.destroy()
        sys.exit(0)


def main():
    """Função principal"""
    try:
        app = SCEEApp()
        app.run()
    except Exception as e:
        logger.error(f"Erro ao iniciar aplicação: {e}", exc_info=True)
        messagebox.showerror("Erro Fatal", f"Não foi possível iniciar a aplicação:\n{e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
