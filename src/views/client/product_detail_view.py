import tkinter as tk
from tkinter import messagebox
from typing import Optional, Callable
from src.config.settings import Config
from src.controllers.cart_controller import CartController
from src.controllers.catalog_controller import CatalogController
from src.views.components.custom_button import CustomButton
from src.views.components.modal_message import ModalMessage


class ProductDetailView(tk.Frame):
    """
    Tela de detalhes do produto.
    Exibe informações completas, imagens, e permite adicionar ao carrinho.
    """
    
    def __init__(
        self, 
        parent, 
        controller, 
        produto_id: int,
        usuario_logado=None,
        on_back: Optional[Callable] = None
    ):
        """
        Args:
            parent: Widget pai
            controller: Controller principal
            produto_id: ID do produto a exibir
            usuario_logado: Usuário logado (para carrinho)
            on_back: Callback para voltar à tela anterior
        """
        super().__init__(parent, bg=Config.COLOR_BG)
        self.controller = controller
        self.produto_id = produto_id
        self.usuario = usuario_logado
        self.on_back = on_back
        
        # Controllers
        self.catalog_controller = CatalogController()
        self.cart_controller = CartController(controller)
        if self.usuario:
            self.cart_controller.set_current_user(self.usuario.id)
        
        # Variável de quantidade
        self.quantidade_var = tk.IntVar(value=1)
        
        # Carregar dados do produto
        self.produto = None
        self.produtos_relacionados = []
        
        self._load_product()
        
        if self.produto:
            self._build_ui()
        else:
            self._show_error()
    
    def _load_product(self):
        """Carrega dados do produto via controller."""
        resultado = self.catalog_controller.get_product_details(self.produto_id)
        
        if resultado['success']:
            self.produto = resultado['data']
            # Carregar produtos relacionados (mesma categoria)
            if self.produto.get('categoria_id'):
                self._load_related_products()
        else:
            print(f"Erro ao carregar produto: {resultado['message']}")
    
    def _load_related_products(self):
        """Carrega produtos da mesma categoria."""
        resultado = self.catalog_controller.list_products(
            categoria_id=self.produto['categoria_id'],
            limit=4
        )
        
        if resultado['success']:
            # Filtrar o produto atual
            self.produtos_relacionados = [
                p for p in resultado['data'] 
                if p['id'] != self.produto_id
            ][:3]  # Máximo 3 produtos
    
    def _build_ui(self):
        """Constrói a interface completa."""
        # Container principal com scroll
        main_container = tk.Frame(self, bg=Config.COLOR_BG)
        main_container.pack(fill="both", expand=True)
        
        # Canvas para scroll
        canvas = tk.Canvas(main_container, bg=Config.COLOR_BG, highlightthickness=0)
        scrollbar = tk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=Config.COLOR_BG)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Conteúdo dentro do scrollable_frame
        self._build_breadcrumb(scrollable_frame)
        self._build_product_section(scrollable_frame)
        self._build_description_section(scrollable_frame)
        
        if self.produtos_relacionados:
            self._build_related_products(scrollable_frame)
    
    def _show_error(self):
        """Exibe mensagem de erro quando produto não é encontrado."""
        tk.Label(
            self,
            text="❌ Produto não encontrado",
            font=Config.FONT_HEADER,
            bg=Config.COLOR_BG,
            fg=Config.COLOR_SECONDARY
        ).pack(pady=50)
        
        if self.on_back:
            CustomButton(
                self,
                text="← Voltar ao Catálogo",
                command=self.on_back,
                style="secondary"
            ).pack(pady=20)
    
    def _build_breadcrumb(self, parent):
        """Breadcrumb de navegação."""
        breadcrumb_frame = tk.Frame(parent, bg=Config.COLOR_BG)
        breadcrumb_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        # Botão Voltar
        if self.on_back:
            btn_voltar = tk.Button(
                breadcrumb_frame,
                text="← Voltar",
                font=Config.FONT_BODY,
                bg=Config.COLOR_BG,
                fg=Config.COLOR_ACCENT,
                bd=0,
                cursor="hand2",
                command=self.on_back
            )
            btn_voltar.pack(side="left")
        
        # Breadcrumb text
        categoria_nome = self.produto.get('categoria_nome', 'Produtos')
        breadcrumb_text = f"  /  {categoria_nome}  /  {self.produto['nome']}"
        
        tk.Label(
            breadcrumb_frame,
            text=breadcrumb_text,
            font=Config.FONT_SMALL,
            bg=Config.COLOR_BG,
            fg=Config.COLOR_TEXT_LIGHT
        ).pack(side="left", padx=(10, 0))
    
    def _build_product_section(self, parent):
        """Seção principal com imagem e informações."""
        main_section = tk.Frame(parent, bg=Config.COLOR_WHITE)
        main_section.pack(fill="x", padx=20, pady=20)
        
        # Grid 2 colunas: Imagem (40%) | Info (60%)
        main_section.columnconfigure(0, weight=2, minsize=300)
        main_section.columnconfigure(1, weight=3, minsize=400)
        
        # COLUNA 1: Imagem
        self._build_image_section(main_section)
        
        # COLUNA 2: Informações
        self._build_info_section(main_section)
    
    def _build_image_section(self, parent):
        """Seção de imagem do produto."""
        image_frame = tk.Frame(parent, bg=Config.COLOR_BG)
        image_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        # Placeholder para imagem (como não temos PIL/Pillow)
        image_container = tk.Frame(
            image_frame,
            bg="#F0F0F0",
            width=300,
            height=300,
            relief="solid",
            bd=1
        )
        image_container.pack()
        image_container.pack_propagate(False)
        
        # Emoji/Ícone representando produto
        tk.Label(
            image_container,
            text="🖼️",
            font=("TkDefaultFont", 72),
            bg="#F0F0F0",
            fg=Config.COLOR_TEXT_LIGHT
        ).place(relx=0.5, rely=0.5, anchor="center")
        
        # URL da imagem (se houver)
        if self.produto.get('imagem_principal'):
            tk.Label(
                image_frame,
                text=f"📎 {self.produto['imagem_principal'][:30]}...",
                font=Config.FONT_SMALL,
                bg=Config.COLOR_BG,
                fg=Config.COLOR_TEXT_LIGHT
            ).pack(pady=(10, 0))
    
    def _build_info_section(self, parent):
        """Seção de informações do produto."""
        info_frame = tk.Frame(parent, bg=Config.COLOR_WHITE)
        info_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        # Nome do produto
        tk.Label(
            info_frame,
            text=self.produto['nome'],
            font=Config.FONT_TITLE,
            bg=Config.COLOR_WHITE,
            fg=Config.COLOR_TEXT,
            wraplength=400,
            justify="left"
        ).pack(anchor="w", pady=(0, 10))
        
        # SKU
        tk.Label(
            info_frame,
            text=f"SKU: {self.produto['sku']}",
            font=Config.FONT_SMALL,
            bg=Config.COLOR_WHITE,
            fg=Config.COLOR_TEXT_LIGHT
        ).pack(anchor="w", pady=(0, 20))
        
        # Preço
        preco_frame = tk.Frame(info_frame, bg=Config.COLOR_WHITE)
        preco_frame.pack(anchor="w", pady=(0, 20))
        
        tk.Label(
            preco_frame,
            text="R$",
            font=Config.FONT_BODY,
            bg=Config.COLOR_WHITE,
            fg=Config.COLOR_TEXT_LIGHT
        ).pack(side="left")
        
        tk.Label(
            preco_frame,
            text=f"{self.produto['preco']:.2f}",
            font=("TkDefaultFont", 28, "bold"),
            bg=Config.COLOR_WHITE,
            fg=Config.COLOR_ACCENT
        ).pack(side="left", padx=(5, 0))
        
        # Estoque
        estoque = self.produto.get('estoque', 0)
        estoque_cor = Config.COLOR_ACCENT if estoque > 5 else Config.COLOR_SECONDARY
        estoque_text = f"✓ {estoque} unidades disponíveis" if estoque > 0 else "✗ Produto esgotado"
        
        tk.Label(
            info_frame,
            text=estoque_text,
            font=Config.FONT_BODY,
            bg=Config.COLOR_WHITE,
            fg=estoque_cor
        ).pack(anchor="w", pady=(0, 30))
        
        # Linha separadora
        tk.Frame(info_frame, bg="#E0E0E0", height=1).pack(fill="x", pady=(0, 20))
        
        # Quantidade e Adicionar ao Carrinho
        if estoque > 0:
            self._build_add_to_cart_section(info_frame, estoque)
        else:
            tk.Label(
                info_frame,
                text="Produto indisponível no momento",
                font=Config.FONT_BODY,
                bg=Config.COLOR_WHITE,
                fg=Config.COLOR_SECONDARY
            ).pack(anchor="w")
    
    def _build_add_to_cart_section(self, parent, estoque_max):
        """Seção de seleção de quantidade e botão adicionar."""
        # Label Quantidade
        tk.Label(
            parent,
            text="Quantidade:",
            font=Config.FONT_BODY,
            bg=Config.COLOR_WHITE,
            fg=Config.COLOR_TEXT
        ).pack(anchor="w", pady=(0, 10))
        
        # Frame quantidade
        qty_frame = tk.Frame(parent, bg=Config.COLOR_WHITE)
        qty_frame.pack(anchor="w", pady=(0, 20))
        
        # Botão diminuir
        btn_minus = tk.Button(
            qty_frame,
            text="−",
            font=Config.FONT_HEADER,
            bg="#E0E0E0",
            fg=Config.COLOR_TEXT,
            width=3,
            bd=0,
            cursor="hand2",
            command=self._decrease_quantity
        )
        btn_minus.pack(side="left", padx=(0, 5))
        
        # Entry quantidade
        self.qty_entry = tk.Entry(
            qty_frame,
            textvariable=self.quantidade_var,
            font=Config.FONT_BODY,
            width=5,
            justify="center",
            bd=1,
            relief="solid"
        )
        self.qty_entry.pack(side="left", padx=5)
        
        # Botão aumentar
        btn_plus = tk.Button(
            qty_frame,
            text="+",
            font=Config.FONT_HEADER,
            bg="#E0E0E0",
            fg=Config.COLOR_TEXT,
            width=3,
            bd=0,
            cursor="hand2",
            command=lambda: self._increase_quantity(estoque_max)
        )
        btn_plus.pack(side="left", padx=(5, 0))
        
        # Label estoque máximo
        tk.Label(
            qty_frame,
            text=f"(máx: {estoque_max})",
            font=Config.FONT_SMALL,
            bg=Config.COLOR_WHITE,
            fg=Config.COLOR_TEXT_LIGHT
        ).pack(side="left", padx=(10, 0))
        
        # Botão Adicionar ao Carrinho
        CustomButton(
            parent,
            text="🛒 Adicionar ao Carrinho",
            command=self._add_to_cart,
            style="primary"
        ).pack(anchor="w", pady=(10, 0), ipadx=20, ipady=5)
    
    def _build_description_section(self, parent):
        """Seção de descrição detalhada."""
        desc_frame = tk.Frame(parent, bg=Config.COLOR_WHITE)
        desc_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Título
        tk.Label(
            desc_frame,
            text="Descrição do Produto",
            font=Config.FONT_HEADER,
            bg=Config.COLOR_WHITE,
            fg=Config.COLOR_TEXT
        ).pack(anchor="w", padx=20, pady=(20, 10))
        
        # Descrição
        descricao = self.produto.get('descricao', 'Sem descrição disponível.')
        
        desc_text = tk.Text(
            desc_frame,
            font=Config.FONT_BODY,
            bg=Config.COLOR_WHITE,
            fg=Config.COLOR_TEXT,
            wrap="word",
            height=6,
            bd=0,
            relief="flat",
            highlightthickness=0
        )
        desc_text.pack(fill="x", padx=20, pady=(0, 20))
        desc_text.insert("1.0", descricao)
        desc_text.config(state="disabled")  # Read-only
        
        # Categoria
        if self.produto.get('categoria_nome'):
            info_grid = tk.Frame(desc_frame, bg=Config.COLOR_WHITE)
            info_grid.pack(fill="x", padx=20, pady=(0, 20))
            
            tk.Label(
                info_grid,
                text="Categoria:",
                font=Config.FONT_BODY,
                bg=Config.COLOR_WHITE,
                fg=Config.COLOR_TEXT_LIGHT
            ).grid(row=0, column=0, sticky="w", pady=5)
            
            tk.Label(
                info_grid,
                text=self.produto['categoria_nome'],
                font=Config.FONT_BODY,
                bg=Config.COLOR_WHITE,
                fg=Config.COLOR_TEXT
            ).grid(row=0, column=1, sticky="w", padx=(10, 0), pady=5)
    
    def _build_related_products(self, parent):
        """Seção de produtos relacionados."""
        related_frame = tk.Frame(parent, bg=Config.COLOR_BG)
        related_frame.pack(fill="x", padx=20, pady=(0, 40))
        
        # Título
        tk.Label(
            related_frame,
            text="Produtos Relacionados",
            font=Config.FONT_HEADER,
            bg=Config.COLOR_BG,
            fg=Config.COLOR_TEXT
        ).pack(anchor="w", pady=(0, 15))
        
        # Grid de produtos
        products_grid = tk.Frame(related_frame, bg=Config.COLOR_BG)
        products_grid.pack(fill="x")
        
        for i, produto in enumerate(self.produtos_relacionados):
            self._build_related_product_card(products_grid, produto, i)
    
    def _build_related_product_card(self, parent, produto, index):
        """Card pequeno de produto relacionado."""
        card = tk.Frame(parent, bg=Config.COLOR_WHITE, relief="solid", bd=1)
        card.grid(row=0, column=index, padx=10, pady=10, sticky="nsew")
        
        parent.columnconfigure(index, weight=1, minsize=200)
        
        # Imagem placeholder
        img_frame = tk.Frame(card, bg="#F5F5F5", height=120)
        img_frame.pack(fill="x", padx=10, pady=10)
        img_frame.pack_propagate(False)
        
        tk.Label(
            img_frame,
            text="🖼️",
            font=("TkDefaultFont", 36),
            bg="#F5F5F5"
        ).pack(expand=True)
        
        # Nome
        tk.Label(
            card,
            text=produto['nome'],
            font=Config.FONT_BODY,
            bg=Config.COLOR_WHITE,
            fg=Config.COLOR_TEXT,
            wraplength=180
        ).pack(padx=10, pady=(0, 5))
        
        # Preço
        tk.Label(
            card,
            text=f"R$ {produto['preco']:.2f}",
            font=("TkDefaultFont", 14, "bold"),
            bg=Config.COLOR_WHITE,
            fg=Config.COLOR_ACCENT
        ).pack(padx=10, pady=(0, 10))
        
        # Botão Ver Detalhes
        btn_ver = tk.Button(
            card,
            text="Ver Detalhes",
            font=Config.FONT_SMALL,
            bg=Config.COLOR_PRIMARY,
            fg=Config.COLOR_WHITE,
            bd=0,
            cursor="hand2",
            command=lambda p_id=produto['id']: self._view_related_product(p_id)
        )
        btn_ver.pack(fill="x", padx=10, pady=(0, 10))
    
    def _view_related_product(self, produto_id):
        """Navega para outro produto relacionado."""
        # Recarregar a mesma view com novo produto_id
        for widget in self.winfo_children():
            widget.destroy()
        
        self.produto_id = produto_id
        self.quantidade_var = tk.IntVar(value=1)
        self._load_product()
        
        if self.produto:
            self._build_ui()
        else:
            self._show_error()
    
    def _increase_quantity(self, max_estoque):
        """Aumenta quantidade (limitado ao estoque)."""
        current = self.quantidade_var.get()
        if current < max_estoque:
            self.quantidade_var.set(current + 1)
    
    def _decrease_quantity(self):
        """Diminui quantidade (mínimo 1)."""
        current = self.quantidade_var.get()
        if current > 1:
            self.quantidade_var.set(current - 1)
    
    def _add_to_cart(self):
        """Adiciona produto ao carrinho."""
        if not self.usuario:
            ModalMessage.show_warning(
                self,
                "Login Necessário",
                "Você precisa estar logado para adicionar produtos ao carrinho."
            )
            return
        
        quantidade = self.quantidade_var.get()
        
        # Validar quantidade
        if quantidade < 1:
            ModalMessage.show_warning(self, "Atenção", "Quantidade deve ser no mínimo 1")
            return
        
        if quantidade > self.produto['estoque']:
            ModalMessage.show_warning(
                self,
                "Estoque Insuficiente",
                f"Apenas {self.produto['estoque']} unidades disponíveis."
            )
            return
        
        # Adicionar ao carrinho
        resultado = self.cart_controller.add_to_cart(
            produto_id=self.produto_id,
            quantidade=quantidade
        )
        
        if resultado['success']:
            ModalMessage.show_success(
                self,
                "Sucesso!",
                f"{quantidade}x {self.produto['nome']} adicionado ao carrinho!"
            )
            # Resetar quantidade
            self.quantidade_var.set(1)
        else:
            ModalMessage.show_error(
                self,
                "Erro",
                resultado['message']
            )
