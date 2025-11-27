import tkinter as tk
from src.config.settings import Config

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(Config.APP_NAME)
        self.geometry(Config.WINDOW_SIZE)
        self.configure(bg=Config.COLOR_BG)
        
        # Container Principal
        self.container = tk.Frame(self, bg=Config.COLOR_BG)
        self.container.pack(fill="both", expand=True)
        
        self.current_view = None
        
        # Inicia no Login
        self.show_view("LoginView")

    def show_view(self, view_name, data=None):
        # Remove a tela anterior
        if self.current_view:
            self.current_view.destroy()

        # Roteamento
        if view_name == "LoginView":
            from src.views.client.login_view import LoginView
            self.current_view = LoginView(self.container, self)
            
        elif view_name == "RegisterView":
            self.current_view = tk.Label(self.container, text="Tela de Cadastro (Em Breve)")
            
        elif view_name == "HomeView":
            # Aqui faremos a Home do cliente depois
            self.current_view = tk.Label(self.container, text=f"LOJA VIRTUAL\nBem vindo cliente: {data.nome if data else 'Visitante'}")
            
        # --- NOVO ---
        elif view_name == "AdminDashboard":
            from src.views.admin.dashboard_view import DashboardView
            # Passamos o objeto usuário (data) para o dashboard saber o nome
            self.current_view = DashboardView(self.container, self, usuario_logado=data)
        # ------------
            
        else:
            self.current_view = tk.Label(self.container, text=f"404 - Tela {view_name} não encontrada")

        self.current_view.pack(fill="both", expand=True)