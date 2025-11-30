import tkinter as tk
from src.config.settings import Config

class ProductCard(tk.Frame):
    """
    Componente visual reutilizável que representa um produto na vitrine.
    """

    def __init__(self, parent, produto, on_add_click, on_details_click=None):
        super().__init__(parent, bg=Config.COLOR_WHITE, bd=1, relief="solid")
        self.produto = produto
        self.on_add_click = on_add_click
        self.on_details_click = on_details_click
        
        self._setup_ui()

    def _setup_ui(self):
        # Container interno com padding (margem interna)
        container = tk.Frame(self, bg=Config.COLOR_WHITE, padx=10, pady=10)
        container.pack(fill="both", expand=True)

        # 1. Nome do Produto (Negrito, quebra linha se for longo)
        tk.Label(
            container, 
            text=self.produto.nome, 
            font=Config.FONT_BODY, 
            bg=Config.COLOR_WHITE,
            fg=Config.COLOR_TEXT,
            wraplength=150, # Quebra o texto se passar de 150 pixels
            justify="left"
        ).pack(anchor="w", pady=(0, 5))

        # 2. Categoria (Cinza, menor)
        nome_cat = self.produto.categoria.nome if self.produto.categoria else "Geral"
        tk.Label(
            container, 
            text=nome_cat, 
            font=Config.FONT_SMALL, 
            bg=Config.COLOR_WHITE,
            fg=Config.COLOR_TEXT_LIGHT
        ).pack(anchor="w")

        # 3. Preço (Grande e Azul)
        tk.Label(
            container, 
            text=f"R$ {self.produto.preco:.2f}", 
            font=Config.FONT_HEADER, 
            bg=Config.COLOR_WHITE,
            fg=Config.COLOR_ACCENT
        ).pack(anchor="w", pady=10)

        # 4. Estoque (Aviso se estiver acabando)
        cor_estoque = Config.COLOR_TEXT_LIGHT
        texto_estoque = f"Estoque: {self.produto.estoque}"
        if self.produto.estoque < 5:
            cor_estoque = Config.COLOR_SECONDARY # Vermelho se baixo
            texto_estoque += " (Últimos!)"
            
        tk.Label(
            container,
            text=texto_estoque,
            font=Config.FONT_SMALL,
            bg=Config.COLOR_WHITE,
            fg=cor_estoque
        ).pack(anchor="w", pady=(0, 10))

        # 5. Botão Ver Detalhes (se callback fornecido)
        if self.on_details_click:
            tk.Button(
                container,
                text="Ver Detalhes",
                bg=Config.COLOR_ACCENT,
                fg="white",
                font=Config.FONT_SMALL,
                cursor="hand2",
                bd=0,
                command=lambda: self.on_details_click(self.produto)
            ).pack(fill="x", pady=(0, 5))
        
        # 6. Botão Comprar
        state = "normal"
        bg_btn = Config.COLOR_PRIMARY
        text_btn = "Adicionar ao Carrinho"
        
        if self.produto.estoque <= 0:
            state = "disabled"
            bg_btn = Config.COLOR_TEXT_LIGHT
            text_btn = "Indisponível"

        tk.Button(
            container,
            text=text_btn,
            bg=bg_btn,
            fg="white",
            font=Config.FONT_SMALL,
            state=state,
            cursor="hand2" if state == "normal" else "arrow",
            command=lambda: self.on_add_click(self.produto)
        ).pack(fill="x")