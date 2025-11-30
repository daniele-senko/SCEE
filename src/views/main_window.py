import tkinter as tk
import os
from src.config.settings import Config
from src.utils.audio_manager import audio_manager

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Configuração para evitar erro X11 BadLength
        # Usa rendering mais simples para fontes
        try:
            self.tk.call('tk', 'scaling', 1.0)
            # Limita cache de fontes para evitar BadLength
            self.option_add('*Font', 'TkDefaultFont')
        except:
            pass
        
        self.title(Config.APP_NAME)
        self.geometry(Config.WINDOW_SIZE)
        self.configure(bg=Config.COLOR_BG)
        
        # Inicializar música de fundo
        self._init_background_music()
        
        # Container Principal
        self.container = tk.Frame(self, bg=Config.COLOR_BG)
        self.container.pack(fill="both", expand=True)
        
        # Controle de áudio (botão discreto no canto)
        self._create_audio_controls()
        
        self.current_view = None
        
        # Inicia no Login
        self.show_view("LoginView")
    
    def _init_background_music(self):
        """Inicializa e toca a música de fundo."""
        # Procura por arquivo de música
        music_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "music")
        
        # Tenta diferentes formatos
        music_files = [
            os.path.join(music_dir, "shopping_background.mp3"),
            os.path.join(music_dir, "shopping_background.ogg"),
            os.path.join(music_dir, "background.mp3"),
            os.path.join(music_dir, "background.ogg"),
        ]
        
        for music_file in music_files:
            if os.path.exists(music_file):
                if audio_manager.set_music(music_file):
                    audio_manager.play(loops=-1)  # Loop infinito
                    print(f"♪ Música de fundo iniciada: {os.path.basename(music_file)}")
                break
    
    def _create_audio_controls(self):
        """Cria controles de áudio discretos."""
        # Frame no canto superior direito
        audio_frame = tk.Frame(self, bg=Config.COLOR_BG)
        audio_frame.place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10)
        
        # Botão de mute/unmute
        self.mute_btn_text = tk.StringVar(value="🔊")
        self.mute_btn = tk.Button(
            audio_frame,
            textvariable=self.mute_btn_text,
            command=self._toggle_music,
            bg=Config.COLOR_PRIMARY,
            fg="white",
            font=("TkDefaultFont", 16),
            relief="flat",
            padx=8,
            pady=4,
            cursor="hand2",
            borderwidth=0
        )
        self.mute_btn.pack(side="right")
        
        # Tooltip
        self._create_tooltip(self.mute_btn, "Música de fundo")
    
    def _toggle_music(self):
        """Alterna música (tocar/pausar)."""
        if audio_manager.is_playing():
            audio_manager.pause()
            self.mute_btn_text.set("🔇")
        else:
            audio_manager.unpause()
            self.mute_btn_text.set("🔊")
    
    def _create_tooltip(self, widget, text):
        """Cria um tooltip simples para o widget."""
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = tk.Label(
                tooltip,
                text=text,
                bg="#333",
                fg="white",
                font=("TkDefaultFont", 9),
                relief="solid",
                borderwidth=1,
                padx=5,
                pady=2
            )
            label.pack()
            
            widget.tooltip = tooltip
        
        def hide_tooltip(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                delattr(widget, 'tooltip')
        
        widget.bind("<Enter>", show_tooltip)
        widget.bind("<Leave>", hide_tooltip)

    def show_view(self, view_name, data=None):
        # Remove a tela anterior
        if self.current_view:
            self.current_view.destroy()

        # Roteamento
        if view_name == "LoginView":
            from src.views.client.login_view import LoginView
            self.current_view = LoginView(self.container, self)
            
        elif view_name == "RegisterView":
            from src.views.client.register_view import RegisterView
            self.current_view = RegisterView(self.container, self)
            
        elif view_name == "HomeView":
            from src.views.client.home_view import HomeView
            self.current_view = HomeView(self.container, self, data=data)

        elif view_name == "AdminDashboard":
            from src.views.admin.dashboard_view import DashboardView
            # Passamos o objeto usuário (data) para o dashboard saber o nome
            self.current_view = DashboardView(self.container, self, usuario_logado=data)

        elif view_name == "ManageProducts":
            from src.views.admin.manage_products_view import ManageProductsView
            self.current_view = ManageProductsView(self.container, self, data=data)
        
        elif view_name == "ManageOrders":
            from src.views.admin.manage_orders_view import ManageOrdersView
            self.current_view = ManageOrdersView(self.container, self, data=data)
        
        elif view_name == "ManageCategories":
            from src.views.admin.manage_categories_view import ManageCategoriesView
            self.current_view = ManageCategoriesView(self.container, self, data=data)

        elif view_name == "ProductFormView":
            from src.views.admin.product_form_view import ProductFormView
            self.current_view = ProductFormView(self.container, self, data=data)
        
        elif view_name == "CartView":
            from src.views.client.cart_view import CartView
            self.current_view = CartView(self.container, self, data=data)
        
        elif view_name == "CheckoutView":
            from src.views.client.checkout_view import CheckoutView
            self.current_view = CheckoutView(self.container, self, data=data)
        
        elif view_name == "MyOrdersView":
            from src.views.client.my_orders_view import MyOrdersView
            self.current_view = MyOrdersView(self.container, self, data=data)
            
        else:
            self.current_view = tk.Label(self.container, text=f"404 - Tela {view_name} não encontrada")

        self.current_view.pack(fill="both", expand=True)