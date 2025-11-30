import tkinter as tk
from tkinter import messagebox, ttk
from src.config.settings import Config
from src.services.catalog_service import CatalogService
from src.views.components.product_card import ProductCard
from src.controllers.cart_controller import CartController

class HomeView(tk.Frame):
    """
    Tela inicial da loja (Catálogo para o Cliente).
    """

    def __init__(self, parent, controller, data=None):
        super().__init__(parent, bg=Config.COLOR_BG)
        self.controller = controller
        self.usuario = data # Usuário logado
        self.service = CatalogService()
        self.cart_controller = CartController(controller)
        if self.usuario:
            self.cart_controller.set_current_user(self.usuario.id)
        
        self._setup_header()
        self._setup_catalog_area()
        # Carrega produtos após renderizar a tela para não travar
        self.after(100, self._load_products)

    def _setup_header(self):
        # Barra Superior
        header = tk.Frame(self, bg=Config.COLOR_PRIMARY, padx=20, pady=15)
        header.pack(fill="x")
        
        # Logo / Título
        tk.Label(
            header, 
            text="SCEE Store", 
            font=Config.FONT_TITLE, 
            bg=Config.COLOR_PRIMARY, 
            fg="white"
        ).pack(side="left")

        # Container de botões do usuário
        user_menu = tk.Frame(header, bg=Config.COLOR_PRIMARY)
        user_menu.pack(side="right")

        # Saudação
        nome = self.usuario.nome.split()[0] if self.usuario else "Visitante"
        tk.Label(
            user_menu, 
            text=f"Olá, {nome}", 
            bg=Config.COLOR_PRIMARY, 
            fg=Config.COLOR_ACCENT,
            font=Config.FONT_BODY,
            padx=10
        ).pack(side="left")

        # Botão Carrinho
        tk.Button(
            user_menu,
            text="🛒 Carrinho",
            bg=Config.COLOR_ACCENT,
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=10,
            command=lambda: self.controller.show_view("CartView", data=self.usuario)
        ).pack(side="left", padx=5)
        
        # Botão Meus Pedidos
        tk.Button(
            user_menu,
            text="📦 Meus Pedidos",
            bg=Config.COLOR_PRIMARY,
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=10,
            command=lambda: self.controller.show_view("MyOrdersView", data=self.usuario)
        ).pack(side="left", padx=5)

        # Botão Sair
        tk.Button(
            user_menu, 
            text="Sair", 
            bg=Config.COLOR_SECONDARY, 
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=10,
            command=lambda: self.controller.show_view("LoginView")
        ).pack(side="left", padx=5)

    def _setup_catalog_area(self):
        """Configura área de rolagem para os produtos."""
        # Título da seção
        tk.Label(
            self, 
            text="Produtos em Destaque", 
            font=Config.FONT_HEADER, 
            bg=Config.COLOR_BG,
            fg=Config.COLOR_TEXT
        ).pack(anchor="w", padx=30, pady=(20, 10))

        # Container de Scroll
        container = tk.Frame(self, bg=Config.COLOR_BG)
        container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.canvas = tk.Canvas(container, bg=Config.COLOR_BG, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        
        self.grid_frame = tk.Frame(self.canvas, bg=Config.COLOR_BG)

        # Configuração do Scroll
        self.grid_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.grid_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Scroll com o mouse
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _load_products(self):
        try:
            produtos = self.service.listar_produtos()
            
            # Limpa produtos antigos
            for widget in self.grid_frame.winfo_children():
                widget.destroy()

            if not produtos:
                tk.Label(
                    self.grid_frame, 
                    text="Nenhum produto disponível no momento.", 
                    bg=Config.COLOR_BG,
                    font=Config.FONT_BODY,
                    fg="gray"
                ).pack(pady=50, padx=50)
                return

            # Grid Responsivo (4 colunas)
            col = 0
            row = 0
            MAX_COLS = 4
            
            for prod in produtos:
                # Filtra apenas ativos
                if isinstance(prod, dict) and not prod.get('ativo'): continue
                if hasattr(prod, 'ativo') and not prod.ativo: continue

                # Cria o card passando a função de adicionar ao carrinho
                card = ProductCard(self.grid_frame, prod, on_add_cart=self._add_to_cart)
                card.grid(row=row, column=col, padx=15, pady=15)
                
                col += 1
                if col >= MAX_COLS:
                    col = 0
                    row += 1
                    
        except Exception as e:
            print(f"Erro home: {e}")
            tk.Label(self.grid_frame, text="Erro ao carregar catálogo.", fg="red").pack()

    def _add_to_cart(self, produto):
        """Adiciona produto ao carrinho."""
        if not self.usuario:
            messagebox.showwarning("Atenção", "Faça login para comprar!")
            return
        
        # Pega ID independente se for Dict ou Objeto
        prod_id = produto.get('id') if isinstance(produto, dict) else produto.id
        nome_prod = produto.get('nome') if isinstance(produto, dict) else produto.nome
        
        res = self.cart_controller.add_to_cart(prod_id, quantidade=1)
        
        if res['success']:
            messagebox.showinfo("Sucesso", f"'{nome_prod}' adicionado ao carrinho!")
        else:
            messagebox.showerror("Erro", res['message'])