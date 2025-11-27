import tkinter as tk
from src.config.settings import Config

class DashboardView(tk.Frame):
    """
    Painel Principal do Administrador.
    Possui um menu lateral e uma área de conteúdo dinâmica.
    """

    def __init__(self, parent, controller, usuario_logado):
        super().__init__(parent, bg=Config.COLOR_BG)
        self.controller = controller
        self.usuario = usuario_logado

        # Layout principal: Sidebar (Esquerda) + Conteúdo (Direita)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self._setup_sidebar()
        self._setup_content_area()

    def _setup_sidebar(self):
        """Cria o menu lateral escuro."""
        sidebar = tk.Frame(self, bg=Config.COLOR_PRIMARY, width=250)
        sidebar.grid(row=0, column=0, sticky="ns")
        sidebar.pack_propagate(False) # Mantém a largura fixa

        # Título do Menu
        tk.Label(
            sidebar, 
            text="PAINEL ADMIN", 
            font=Config.FONT_HEADER, 
            bg=Config.COLOR_PRIMARY, 
            fg=Config.COLOR_WHITE
        ).pack(pady=30)

        # Info do Usuário
        tk.Label(
            sidebar,
            text=f"Olá, {self.usuario.nome.split()[0]}",
            font=Config.FONT_BODY,
            bg=Config.COLOR_PRIMARY,
            fg=Config.COLOR_ACCENT
        ).pack(pady=(0, 20))

        # Botões de Navegação (Estilo Flat)
        self._create_nav_button(sidebar, "📦 Gerenciar Produtos", "ManageProducts")
        self._create_nav_button(sidebar, "🛒 Ver Pedidos", "ManageOrders")
        self._create_nav_button(sidebar, "🔐 Sair / Logout", "Logout", color=Config.COLOR_SECONDARY)

    def _create_nav_button(self, parent, text, action, color=None):
        """Helper para criar botões padronizados no menu."""
        btn = tk.Button(
            parent,
            text=text,
            font=Config.FONT_BODY,
            bg=color if color else Config.COLOR_PRIMARY,
            fg=Config.COLOR_WHITE,
            bd=0,
            activebackground=Config.COLOR_ACCENT,
            activeforeground=Config.COLOR_WHITE,
            cursor="hand2",
            anchor="w",
            padx=20,
            command=lambda: self._handle_navigation(action)
        )
        btn.pack(fill="x", pady=2, ipady=10)

    def _setup_content_area(self):
        """Área onde os gráficos ou tabelas aparecerão."""
        content = tk.Frame(self, bg=Config.COLOR_BG, padx=40, pady=40)
        content.grid(row=0, column=1, sticky="nsew")

        tk.Label(
            content, 
            text="Visão Geral da Loja", 
            font=Config.FONT_TITLE, 
            bg=Config.COLOR_BG, 
            fg=Config.COLOR_TEXT
        ).pack(anchor="w")

        # Cards de Estatísticas (Mockup)
        stats_frame = tk.Frame(content, bg=Config.COLOR_BG)
        stats_frame.pack(fill="x", pady=20)

        self._create_stat_card(stats_frame, "Total Vendas", "R$ 0,00", Config.COLOR_ACCENT)
        self._create_stat_card(stats_frame, "Pedidos Pendentes", "0", Config.COLOR_SECONDARY)
        self._create_stat_card(stats_frame, "Produtos Ativos", "0", Config.COLOR_PRIMARY)

    def _create_stat_card(self, parent, title, value, color):
        card = tk.Frame(parent, bg=Config.COLOR_WHITE, padx=20, pady=20)
        card.pack(side="left", padx=10, expand=True, fill="x")
        
        # Borda colorida à esquerda
        strip = tk.Frame(card, bg=color, width=5)
        strip.pack(side="left", fill="y", padx=(0, 10))

        tk.Label(card, text=title, font=Config.FONT_SMALL, bg=Config.COLOR_WHITE, fg=Config.COLOR_TEXT_LIGHT).pack(anchor="w")
        tk.Label(card, text=value, font=Config.FONT_HEADER, bg=Config.COLOR_WHITE, fg=Config.COLOR_TEXT).pack(anchor="w")

    def _handle_navigation(self, action):
        if action == "Logout":
            self.controller.show_view("LoginView")
        else:
            # Futuro: Navegar para outras telas de admin
            print(f"Navegar para {action}")