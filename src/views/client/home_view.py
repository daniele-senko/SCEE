import tkinter as tk
from tkinter import messagebox, ttk
from src.config.settings import Config
from src.services.catalog_service import CatalogService
from src.views.components.product_card import ProductCard
from src.controllers.cart_controller import CartController


class HomeView(tk.Frame):
    """
    Tela inicial da loja (Catálogo para o Cliente).
    Inclui Busca, Filtro de Categoria e Filtro de Preço (RF05).
    """

    def __init__(self, parent, controller, data=None):
        super().__init__(parent, bg=Config.COLOR_BG)
        self.controller = controller
        self.usuario = data  # Usuário logado
        self.service = CatalogService()
        self.cart_controller = CartController(controller)

        if self.usuario:
            self.cart_controller.set_current_user(self.usuario.id)

        self.todos_produtos = []

        self._setup_header()
        self._setup_filters()
        self._setup_catalog_area()

        # Carrega produtos após renderizar a tela
        self.after(100, self._load_products)

    def _setup_header(self):
        header = tk.Frame(self, bg=Config.COLOR_PRIMARY, padx=20, pady=15)
        header.pack(fill="x")

        tk.Label(
            header,
            text="SCEE Store",
            font=Config.FONT_TITLE,
            bg=Config.COLOR_PRIMARY,
            fg="white",
        ).pack(side="left")

        user_menu = tk.Frame(header, bg=Config.COLOR_PRIMARY)
        user_menu.pack(side="right")

        nome = self.usuario.nome.split()[0] if self.usuario else "Visitante"
        tk.Label(
            user_menu,
            text=f"Olá, {nome}",
            bg=Config.COLOR_PRIMARY,
            fg=Config.COLOR_ACCENT,
            font=Config.FONT_BODY,
            padx=10,
        ).pack(side="left")

        tk.Button(
            user_menu,
            text="🛒 Carrinho",
            bg=Config.COLOR_ACCENT,
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=10,
            command=lambda: self.controller.show_view("CartView", data=self.usuario),
        ).pack(side="left", padx=5)

        tk.Button(
            user_menu,
            text="📦 Meus Pedidos",
            bg=Config.COLOR_PRIMARY,
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=10,
            command=lambda: self.controller.show_view(
                "MyOrdersView", data=self.usuario
            ),
        ).pack(side="left", padx=5)

        tk.Button(
            user_menu,
            text="Sair",
            bg=Config.COLOR_SECONDARY,
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=10,
            command=lambda: self.controller.show_view("LoginView"),
        ).pack(side="left", padx=5)

    def _setup_filters(self):
        """Barra de Pesquisa e Filtros (RF05)."""
        filter_frame = tk.Frame(
            self, bg="white", padx=20, pady=15, relief="solid", bd=1
        )
        filter_frame.pack(fill="x", padx=20, pady=(20, 0))

        # --- Busca por Nome ---
        tk.Label(
            filter_frame, text="🔍 Buscar:", bg="white", font=Config.FONT_BODY
        ).pack(side="left")

        self.ent_busca = tk.Entry(
            filter_frame, width=25, font=Config.FONT_BODY, bg="#F5F5F5", relief="flat"
        )
        self.ent_busca.pack(side="left", padx=(5, 15), ipady=3)
        self.ent_busca.bind("<KeyRelease>", self._aplicar_filtros)

        # --- Filtro por Categoria ---
        tk.Label(
            filter_frame, text="📂 Categoria:", bg="white", font=Config.FONT_BODY
        ).pack(side="left")

        self.combo_categoria = ttk.Combobox(filter_frame, state="readonly", width=20)
        self.combo_categoria.pack(side="left", padx=(5, 15))
        self.combo_categoria.bind("<<ComboboxSelected>>", self._aplicar_filtros)

        # --- Filtro por Preço (NOVO) ---
        tk.Label(
            filter_frame, text="💰 Preço:", bg="white", font=Config.FONT_BODY
        ).pack(side="left")

        self.combo_preco = ttk.Combobox(
            filter_frame,
            state="readonly",
            width=15,
            values=[
                "Todos",
                "Até R$ 50",
                "R$ 50 - R$ 100",
                "R$ 100 - R$ 300",
                "Acima de R$ 300",
            ],
        )
        self.combo_preco.pack(side="left", padx=(5, 15))
        self.combo_preco.current(0)
        self.combo_preco.bind("<<ComboboxSelected>>", self._aplicar_filtros)

        # Botão Limpar
        tk.Button(
            filter_frame,
            text="Limpar Filtros",
            command=self._limpar_filtros,
            bg="#E5E7EB",
            fg="#374151",
            bd=0,
            cursor="hand2",
            font=Config.FONT_SMALL,
        ).pack(side="right")

    def _setup_catalog_area(self):
        """Configura área de rolagem para os produtos."""
        tk.Label(
            self,
            text="Catálogo de Produtos",
            font=Config.FONT_HEADER,
            bg=Config.COLOR_BG,
            fg=Config.COLOR_TEXT,
        ).pack(anchor="w", padx=30, pady=(15, 10))

        container = tk.Frame(self, bg=Config.COLOR_BG)
        container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.canvas = tk.Canvas(container, bg=Config.COLOR_BG, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(
            container, orient="vertical", command=self.canvas.yview
        )

        self.grid_frame = tk.Frame(self.canvas, bg=Config.COLOR_BG)

        self.grid_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.canvas.create_window((0, 0), window=self.grid_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _load_products(self):
        try:
            self.todos_produtos = self.service.listar_produtos()
            self._carregar_categorias_filtro()
            self._update_grid(self.todos_produtos)

        except Exception as e:
            print(f"Erro home: {e}")
            tk.Label(
                self.grid_frame, text="Erro ao carregar catálogo.", fg="red"
            ).pack()

    def _carregar_categorias_filtro(self):
        categorias = set()
        for p in self.todos_produtos:
            cat = getattr(p, "categoria", None)
            nome_cat = None

            if cat and hasattr(cat, "nome"):
                nome_cat = cat.nome
            elif isinstance(p, dict) and p.get("categoria_nome"):
                nome_cat = p["categoria_nome"]

            if nome_cat:
                categorias.add(nome_cat)

        lista_cats = sorted(list(categorias))
        self.combo_categoria["values"] = ["Todas"] + lista_cats
        self.combo_categoria.current(0)

    def _aplicar_filtros(self, event=None):
        """Filtra a lista localmente (Nome, Categoria e Preço)."""
        termo = self.ent_busca.get().lower().strip()
        cat_selecionada = self.combo_categoria.get()
        preco_selecionado = self.combo_preco.get()

        produtos_filtrados = []

        for p in self.todos_produtos:
            # 1. Filtro Nome
            nome = getattr(p, "nome", "").lower()
            match_nome = termo in nome

            # 2. Filtro Categoria
            cat_obj = getattr(p, "categoria", None)
            cat_nome = cat_obj.nome if cat_obj and hasattr(cat_obj, "nome") else ""
            match_cat = (cat_selecionada == "Todas" or cat_selecionada == "") or (
                cat_nome == cat_selecionada
            )

            # 3. Filtro Preço (Lógica Simples)
            preco = getattr(p, "preco", 0.0)
            match_preco = True

            if preco_selecionado == "Até R$ 50":
                match_preco = preco <= 50
            elif preco_selecionado == "R$ 50 - R$ 100":
                match_preco = 50 <= preco <= 100
            elif preco_selecionado == "R$ 100 - R$ 300":
                match_preco = 100 <= preco <= 300
            elif preco_selecionado == "Acima de R$ 300":
                match_preco = preco > 300

            # 4. Filtro Ativo
            ativo = getattr(p, "ativo", 1)

            if match_nome and match_cat and match_preco and ativo:
                produtos_filtrados.append(p)

        self._update_grid(produtos_filtrados)

    def _limpar_filtros(self):
        """Reseta todos os filtros."""
        self.ent_busca.delete(0, tk.END)
        self.combo_categoria.current(0)
        self.combo_preco.current(0)
        self._aplicar_filtros()

    def _update_grid(self, produtos):
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        if not produtos:
            tk.Label(
                self.grid_frame,
                text="Nenhum produto encontrado com estes filtros.",
                bg=Config.COLOR_BG,
                font=Config.FONT_BODY,
                fg="gray",
            ).pack(pady=50)
            return

        col = 0
        row = 0
        MAX_COLS = 4

        for prod in produtos:
            card = ProductCard(self.grid_frame, prod, on_add_cart=self._add_to_cart)
            card.grid(row=row, column=col, padx=15, pady=15)

            col += 1
            if col >= MAX_COLS:
                col = 0
                row += 1

    def _add_to_cart(self, produto):
        if not self.usuario:
            messagebox.showwarning("Atenção", "Faça login para comprar!")
            return

        prod_id = produto.get("id") if isinstance(produto, dict) else produto.id
        nome_prod = produto.get("nome") if isinstance(produto, dict) else produto.nome

        res = self.cart_controller.add_to_cart(prod_id, quantidade=1)

        if res["success"]:
            messagebox.showinfo("Sucesso", f"'{nome_prod}' adicionado ao carrinho!")
        else:
            messagebox.showerror("Erro", res["message"])
