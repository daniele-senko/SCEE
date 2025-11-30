import tkinter as tk
from tkinter import messagebox
from src.config.settings import Config
from src.services.catalog_service import CatalogService
from src.views.components.product_card import ProductCard

class HomeView(tk.Frame):
    """
    Tela inicial da loja (Catálogo para o Cliente).
    """

    def __init__(self, parent, controller, data=None):
        super().__init__(parent, bg=Config.COLOR_BG)
        self.controller = controller
        self.usuario = data # Usuário logado
        self.service = CatalogService()
        
        self._setup_header()
        self._setup_grid()
        self._load_products()

    def _setup_header(self):
        # Barra Superior
        header = tk.Frame(self, bg=Config.COLOR_PRIMARY, padx=20, pady=15)
        header.pack(fill="x")
        
        # Logo / Título
        tk.Label(
            header, 
            text="SCEE Store", 
            font=Config.FONT_HEADER, 
            bg=Config.COLOR_PRIMARY, 
            fg="white"
        ).pack(side="left")

        # Menu Usuário
        info_user = f"Olá, {self.usuario.nome.split()[0]}" if self.usuario else "Visitante"
        tk.Label(header, text=info_user, bg=Config.COLOR_PRIMARY, fg="white").pack(side="right", padx=10)

        # Botão Sair
        tk.Button(
            header, 
            text="Sair", 
            bg=Config.COLOR_SECONDARY, 
            fg="white",
            font=Config.FONT_SMALL,
            command=lambda: self.controller.show_view("LoginView")
        ).pack(side="right")
        
        # Botão Meus Pedidos
        tk.Button(
            header,
            text="Meus Pedidos",
            bg=Config.COLOR_ACCENT,
            fg="white",
            font=Config.FONT_SMALL,
            command=lambda: self.controller.show_view("MyOrdersView", data=self.usuario)
        ).pack(side="right", padx=10)
        
        # Botão Carrinho
        tk.Button(
            header,
            text="Carrinho",
            bg=Config.COLOR_ACCENT,
            fg="white",
            font=Config.FONT_SMALL,
            command=lambda: self.controller.show_view("CartView", data=self.usuario)
        ).pack(side="right", padx=10)

    def _setup_grid(self):
        """Área onde os produtos ficam (com scroll)."""
        # Container principal com padding
        self.main_container = tk.Frame(self, bg=Config.COLOR_BG, padx=20, pady=20)
        self.main_container.pack(fill="both", expand=True)
        
        tk.Label(
            self.main_container, 
            text="Produtos em Destaque", 
            font=Config.FONT_HEADER, 
            bg=Config.COLOR_BG
        ).pack(anchor="w", pady=(0, 20))

        # Frame para os cards (Grid)
        self.grid_frame = tk.Frame(self.main_container, bg=Config.COLOR_BG)
        self.grid_frame.pack(fill="both", expand=True)

    def _load_products(self):
        try:
            produtos = self.service.listar_produtos()
            
            if not produtos:
                tk.Label(self.grid_frame, text="Nenhum produto disponível.", bg=Config.COLOR_BG).pack()
                return

            # Lógica de Grid (Colunas e Linhas)
            col = 0
            row = 0
            MAX_COLS = 4 # Quantos produtos por linha
            
            for prod in produtos:
                # Cria o card passando a função de clique
                card = ProductCard(self.grid_frame, prod, self._add_to_cart)
                card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
                
                col += 1
                if col >= MAX_COLS:
                    col = 0
                    row += 1
                    
        except Exception as e:
            print(f"Erro ao carregar home: {e}")
            tk.Label(self.grid_frame, text="Erro ao carregar catálogo.", fg="red").pack()

    def _add_to_cart(self, produto):
        """Callback quando clica em comprar no card."""
        from src.controllers.cart_controller import CartController
        
        if not self.usuario:
            messagebox.showwarning("Atenção", "Você precisa estar logado para adicionar ao carrinho!")
            return
        
        cart_controller = CartController(self.controller)
        cart_controller.set_current_user(self.usuario.id)
        
        resultado = cart_controller.add_to_cart(produto.id, quantidade=1)
        
        if resultado['success']:
            messagebox.showinfo("Sucesso", f"{produto.nome} adicionado ao carrinho!")
        else:
            messagebox.showerror("Erro", resultado['message'])