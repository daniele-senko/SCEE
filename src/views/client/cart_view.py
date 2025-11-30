import tkinter as tk
from tkinter import messagebox
from src.config.settings import Config
from src.controllers.cart_controller import CartController
from decimal import Decimal


class CartView(tk.Frame):
    """
    Tela do Carrinho de Compras.
    Exibe os itens do carrinho e permite gerenciar quantidades.
    """

    def __init__(self, parent, controller, data=None):
        super().__init__(parent, bg=Config.COLOR_BG)
        self.controller = controller
        self.usuario = data  # Usuário logado
        self.cart_controller = CartController(controller)
        
        if self.usuario:
            self.cart_controller.set_current_user(self.usuario.id)
        
        self._setup_header()
        self._setup_content()
        self._load_cart()

    def _setup_header(self):
        """Barra superior com título e navegação."""
        header = tk.Frame(self, bg=Config.COLOR_PRIMARY, padx=20, pady=15)
        header.pack(fill="x")
        
        # Título
        tk.Label(
            header, 
            text="Meu Carrinho", 
            font=Config.FONT_HEADER, 
            bg=Config.COLOR_PRIMARY, 
            fg="white"
        ).pack(side="left")

        # Botão Voltar
        tk.Button(
            header, 
            text="← Continuar Comprando", 
            bg=Config.COLOR_ACCENT, 
            fg="white",
            font=Config.FONT_SMALL,
            command=lambda: self.controller.show_view("HomeView", data=self.usuario)
        ).pack(side="right")

    def _setup_content(self):
        """Área principal com lista de itens e resumo."""
        # Container principal
        self.main_container = tk.Frame(self, bg=Config.COLOR_BG, padx=20, pady=20)
        self.main_container.pack(fill="both", expand=True)
        
        # Frame para itens do carrinho (com scroll)
        self.items_frame = tk.Frame(self.main_container, bg=Config.COLOR_BG)
        self.items_frame.pack(side="left", fill="both", expand=True, padx=(0, 20))
        
        # Frame lateral para resumo
        self.summary_frame = tk.Frame(
            self.main_container, 
            bg=Config.COLOR_WHITE, 
            width=300,
            padx=20,
            pady=20
        )
        self.summary_frame.pack(side="right", fill="y")
        self.summary_frame.pack_propagate(False)

    def _load_cart(self):
        """Carrega os itens do carrinho."""
        if not self.usuario:
            tk.Label(
                self.items_frame, 
                text="Você precisa estar logado para ver o carrinho.",
                font=Config.FONT_BODY,
                bg=Config.COLOR_BG
            ).pack(pady=20)
            return
        
        # Busca o carrinho do usuário
        resultado = self.cart_controller.get_cart()
        
        print(f"DEBUG CartView: Resultado get_cart = {resultado}")
        
        if not resultado['success']:
            tk.Label(
                self.items_frame,
                text="Erro ao carregar carrinho.",
                font=Config.FONT_BODY,
                bg=Config.COLOR_BG,
                fg=Config.COLOR_SECONDARY
            ).pack(pady=20)
            return
        
        carrinho = resultado.get('data')
        print(f"DEBUG CartView: Carrinho data = {carrinho}")
        print(f"DEBUG CartView: Itens = {carrinho.get('itens') if carrinho else 'None'}")
        
        if not carrinho or not carrinho.get('itens'):
            # Carrinho vazio
            tk.Label(
                self.items_frame,
                text="Seu carrinho está vazio",
                font=Config.FONT_HEADER,
                bg=Config.COLOR_BG
            ).pack(pady=40)
            
            tk.Label(
                self.items_frame,
                text="Adicione produtos para começar suas compras!",
                font=Config.FONT_BODY,
                bg=Config.COLOR_BG,
                fg=Config.COLOR_TEXT_LIGHT
            ).pack()
            
            self._show_summary(Decimal('0.00'), 0)
            return
        
        # Título da lista
        tk.Label(
            self.items_frame,
            text="Itens no Carrinho",
            font=Config.FONT_HEADER,
            bg=Config.COLOR_BG
        ).pack(anchor="w", pady=(0, 10))
        
        # Renderiza cada item
        itens = carrinho.get('itens', [])
        for item in itens:
            self._create_item_card(item)
        
        # Mostra resumo com total
        total = carrinho.get('total', Decimal('0.00'))
        quantidade_total = sum(item.get('quantidade', 0) for item in itens)
        self._show_summary(total, quantidade_total)

    def _create_item_card(self, item: dict):
        """Cria um card para cada item do carrinho."""
        card = tk.Frame(self.items_frame, bg=Config.COLOR_WHITE, padx=15, pady=15)
        card.pack(fill="x", pady=5)
        
        # Nome do produto
        tk.Label(
            card,
            text=item.get('nome_produto', 'Produto'),
            font=Config.FONT_HEADER,
            bg=Config.COLOR_WHITE,
            fg=Config.COLOR_TEXT
        ).grid(row=0, column=0, sticky="w", padx=(0, 10))
        
        # Preço unitário
        preco = item.get('preco_unitario', Decimal('0.00'))
        tk.Label(
            card,
            text=f"R$ {preco:.2f}",
            font=Config.FONT_BODY,
            bg=Config.COLOR_WHITE,
            fg=Config.COLOR_TEXT_LIGHT
        ).grid(row=1, column=0, sticky="w")
        
        # Controles de quantidade
        qty_frame = tk.Frame(card, bg=Config.COLOR_WHITE)
        qty_frame.grid(row=0, column=1, rowspan=2, padx=10)
        
        item_id = item.get('id')
        quantidade_atual = item.get('quantidade', 1)
        
        # Botão diminuir
        tk.Button(
            qty_frame,
            text="-",
            width=2,
            bg=Config.COLOR_BG,
            command=lambda: self._decrease_quantity(item_id, quantidade_atual)
        ).pack(side="left", padx=2)
        
        # Label quantidade
        tk.Label(
            qty_frame,
            text=str(quantidade_atual),
            font=Config.FONT_BODY,
            bg=Config.COLOR_WHITE,
            width=3
        ).pack(side="left", padx=5)
        
        # Botão aumentar
        tk.Button(
            qty_frame,
            text="+",
            width=2,
            bg=Config.COLOR_BG,
            command=lambda: self._increase_quantity(item_id, quantidade_atual)
        ).pack(side="left", padx=2)
        
        # Subtotal do item
        subtotal = preco * quantidade_atual
        tk.Label(
            card,
            text=f"R$ {subtotal:.2f}",
            font=Config.FONT_HEADER,
            bg=Config.COLOR_WHITE,
            fg=Config.COLOR_PRIMARY
        ).grid(row=0, column=2, rowspan=2, padx=10)
        
        # Botão remover
        tk.Button(
            card,
            text="🗑",
            bg=Config.COLOR_SECONDARY,
            fg="white",
            width=3,
            command=lambda: self._remove_item(item_id)
        ).grid(row=0, column=3, rowspan=2, padx=5)

    def _show_summary(self, total: Decimal, quantidade_itens: int):
        """Exibe o resumo do carrinho no painel lateral."""
        tk.Label(
            self.summary_frame,
            text="Resumo do Pedido",
            font=Config.FONT_HEADER,
            bg=Config.COLOR_WHITE,
            fg=Config.COLOR_TEXT
        ).pack(anchor="w", pady=(0, 20))
        
        # Quantidade de itens
        tk.Label(
            self.summary_frame,
            text=f"Itens: {quantidade_itens}",
            font=Config.FONT_BODY,
            bg=Config.COLOR_WHITE
        ).pack(anchor="w", pady=5)
        
        # Subtotal
        tk.Label(
            self.summary_frame,
            text=f"Subtotal: R$ {total:.2f}",
            font=Config.FONT_BODY,
            bg=Config.COLOR_WHITE
        ).pack(anchor="w", pady=5)
        
        # Linha divisória
        tk.Frame(self.summary_frame, height=1, bg=Config.COLOR_BG).pack(fill="x", pady=10)
        
        # Total
        tk.Label(
            self.summary_frame,
            text=f"Total: R$ {total:.2f}",
            font=Config.FONT_TITLE,
            bg=Config.COLOR_WHITE,
            fg=Config.COLOR_PRIMARY
        ).pack(anchor="w", pady=(10, 20))
        
        # Botões de ação
        if quantidade_itens > 0:
            tk.Button(
                self.summary_frame,
                text="FINALIZAR COMPRA",
                font=Config.FONT_HEADER,
                bg=Config.COLOR_PRIMARY,
                fg="white",
                width=20,
                cursor="hand2",
                command=self._go_to_checkout
            ).pack(pady=10)
            
            tk.Button(
                self.summary_frame,
                text="Limpar Carrinho",
                font=Config.FONT_SMALL,
                bg=Config.COLOR_SECONDARY,
                fg="white",
                width=20,
                cursor="hand2",
                command=self._clear_cart
            ).pack(pady=5)

    def _increase_quantity(self, item_id: int, current_qty: int):
        """Aumenta a quantidade de um item."""
        resultado = self.cart_controller.update_quantity(item_id, current_qty + 1)
        
        if resultado['success']:
            self._reload_cart()
        else:
            messagebox.showerror("Erro", resultado['message'])

    def _decrease_quantity(self, item_id: int, current_qty: int):
        """Diminui a quantidade de um item."""
        if current_qty <= 1:
            # Se já está em 1, pergunta se quer remover
            if messagebox.askyesno("Remover", "Deseja remover este item do carrinho?"):
                self._remove_item(item_id)
        else:
            resultado = self.cart_controller.update_quantity(item_id, current_qty - 1)
            
            if resultado['success']:
                self._reload_cart()
            else:
                messagebox.showerror("Erro", resultado['message'])

    def _remove_item(self, item_id: int):
        """Remove um item do carrinho."""
        resultado = self.cart_controller.remove_from_cart(item_id)
        
        if resultado['success']:
            messagebox.showinfo("Sucesso", "Item removido do carrinho")
            self._reload_cart()
        else:
            messagebox.showerror("Erro", resultado['message'])

    def _clear_cart(self):
        """Limpa todo o carrinho."""
        if messagebox.askyesno("Confirmar", "Deseja realmente limpar todo o carrinho?"):
            resultado = self.cart_controller.clear_cart()
            
            if resultado['success']:
                messagebox.showinfo("Sucesso", "Carrinho limpo")
                self._reload_cart()
            else:
                messagebox.showerror("Erro", resultado['message'])

    def _go_to_checkout(self):
        """Navega para a tela de checkout."""
        self.controller.show_view("CheckoutView", data=self.usuario)

    def _reload_cart(self):
        """Recarrega a visualização do carrinho."""
        # Limpa frames
        for widget in self.items_frame.winfo_children():
            widget.destroy()
        
        for widget in self.summary_frame.winfo_children():
            widget.destroy()
        
        # Recarrega
        self._load_cart()
