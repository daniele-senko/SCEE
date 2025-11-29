import tkinter as tk
from src.config.settings import Config

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Configuração para evitar erro X11 BadLength
        # Usa rendering mais simples para fontes
        try:
            self.tk.call('tk', 'scaling', 1.0)
        except:
            pass
        
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
            from src.views.client.home_view import HomeView
            self.current_view = HomeView(self.container, self, data=data)

        elif view_name == "AdminDashboard":
            from src.views.admin.dashboard_view import DashboardView
            # Passamos o objeto usuário (data) para o dashboard saber o nome
            self.current_view = DashboardView(self.container, self, usuario_logado=data)

        elif view_name == "ManageProducts":
            from src.views.admin.manage_products_view import ManageProductsView
            self.current_view = ManageProductsView(self.container, self)

        elif view_name == "ProductFormView":
            from src.views.admin.product_form_view import ProductFormView
            self.current_view = ProductFormView(self.container, self)
            
        else:
            self.current_view = tk.Label(self.container, text=f"404 - Tela {view_name} não encontrada")

        self.current_view.pack(fill="both", expand=True)