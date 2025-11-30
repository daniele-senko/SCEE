import tkinter as tk
from src.config.settings import Config
from src.controllers.admin_controller import AdminController

class DashboardView(tk.Frame):
    """
    Painel Principal do Administrador.
    Exibe estatísticas em tempo real e menu de navegação.
    """

    def __init__(self, parent, controller, usuario_logado):
        super().__init__(parent, bg=Config.COLOR_BG)
        self.controller = controller
        self.usuario = usuario_logado
        
        # --- Inicializa o Controller para buscar dados ---
        self.admin_controller = AdminController(controller)
        if hasattr(self.usuario, 'id'):
            self.admin_controller.set_current_admin(self.usuario.id)

        # Layout principal: Sidebar (Esquerda) + Conteúdo (Direita)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self._setup_sidebar()
        self._setup_content_area()
        
        # --- Carrega os dados reais após 100ms ---
        self.after(100, self._load_statistics)

    def _setup_sidebar(self):
        """Cria o menu lateral escuro."""
        sidebar = tk.Frame(self, bg=Config.COLOR_PRIMARY, width=250)
        sidebar.grid(row=0, column=0, sticky="ns")
        sidebar.pack_propagate(False)

        # Título do Menu
        tk.Label(
            sidebar, 
            text="PAINEL ADMIN", 
            font=Config.FONT_HEADER, 
            bg=Config.COLOR_PRIMARY, 
            fg=Config.COLOR_WHITE
        ).pack(pady=30)

        # Info do Usuário
        nome_display = self.usuario.nome.split()[0] if self.usuario and self.usuario.nome else "Admin"
        tk.Label(
            sidebar,
            text=f"Olá, {nome_display}",
            font=Config.FONT_BODY,
            bg=Config.COLOR_PRIMARY,
            fg=Config.COLOR_ACCENT
        ).pack(pady=(0, 20))

        # Botões de Navegação
        self._create_nav_button(sidebar, "Gerenciar Produtos", "ManageProducts")
        self._create_nav_button(sidebar, "Gerenciar Categorias", "ManageCategories")
        self._create_nav_button(sidebar, "Ver Pedidos", "ManageOrders")
        self._create_nav_button(sidebar, "Sair / Logout", "Logout", color=Config.COLOR_SECONDARY)

    def _create_nav_button(self, parent, text, action, color=None):
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

        # Container dos Cards
        stats_frame = tk.Frame(content, bg=Config.COLOR_BG)
        stats_frame.pack(fill="x", pady=20)

        # --- Guardamos as referências das labels para atualizar depois ---
        self.lbl_vendas = self._create_stat_card(stats_frame, "Total Vendas", "R$ ...", Config.COLOR_ACCENT)
        self.lbl_pedidos = self._create_stat_card(stats_frame, "Pedidos Pendentes", "...", Config.COLOR_SECONDARY)
        self.lbl_produtos = self._create_stat_card(stats_frame, "Produtos Ativos", "...", Config.COLOR_PRIMARY)

    def _create_stat_card(self, parent, title, value, color):
        """
        Cria o card e RETORNA a Label do valor para podermos mudar o texto depois.
        """
        card = tk.Frame(parent, bg=Config.COLOR_WHITE, padx=20, pady=20)
        card.pack(side="left", padx=10, expand=True, fill="x")
        
        # Borda colorida à esquerda
        strip = tk.Frame(card, bg=color, width=5)
        strip.pack(side="left", fill="y", padx=(0, 10))

        tk.Label(card, text=title, font=Config.FONT_SMALL, bg=Config.COLOR_WHITE, fg=Config.COLOR_TEXT_LIGHT).pack(anchor="w")
        
        # Label do Valor (é esta que retornamos)
        lbl_value = tk.Label(card, text=value, font=Config.FONT_HEADER, bg=Config.COLOR_WHITE, fg=Config.COLOR_TEXT)
        lbl_value.pack(anchor="w")
        
        return lbl_value

    def _load_statistics(self):
        """
        Busca dados reais do banco e atualiza a tela.
        """
        try:
            resultado = self.admin_controller.get_dashboard_stats()
            
            if resultado['success']:
                stats = resultado['data']
                
                # Atualiza os textos das labels com os dados do banco
                total = stats.get('total_vendas', 0.0) or 0.0
                pendentes = stats.get('pedidos_pendentes', 0)
                produtos = stats.get('total_produtos', 0)
                
                self.lbl_vendas.config(text=f"R$ {total:.2f}")
                self.lbl_pedidos.config(text=str(pendentes))
                self.lbl_produtos.config(text=str(produtos))
            else:
                print(f"Erro ao carregar stats: {resultado['message']}")
                
        except Exception as e:
            print(f"Erro crítico no dashboard: {e}")

    def _handle_navigation(self, action):
        """Gerencia a troca de telas baseada no botão clicado."""
        if action == "Logout":
            self.controller.show_view("LoginView")
        elif action == "ManageProducts":
            self.controller.show_view("ManageProducts", data=self.usuario)
        elif action == "ManageCategories":
            self.controller.show_view("ManageCategories", data=self.usuario)
        elif action == "ManageOrders":
            self.controller.show_view("ManageOrders", data=self.usuario)
        else:
            print(f"Ação desconhecida: {action}")