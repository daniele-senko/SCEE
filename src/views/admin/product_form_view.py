import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import traceback
from src.config.settings import Config
from src.services.catalog_service import CatalogService


class ProductFormView(tk.Frame):
    """
    Formulário para Adicionar ou Editar Produtos (Compatível com Objetos e Dicts).
    """

    def __init__(self, parent, controller, data=None):
        super().__init__(parent, bg=Config.COLOR_BG)
        self.controller = controller

        # Extração segura dos dados
        if isinstance(data, dict) and "usuario" in data:
            self.usuario = data["usuario"]
            self.produto = data.get("produto", None)
        else:
            self.usuario = data
            self.produto = None

        self.service = CatalogService()
        self.categorias_map = {}
        self.imagem_path = None

        self._setup_ui()
        self.after(100, self._load_categories)

    def _get_val(self, obj, key, default=None):
        """Helper para pegar valor de Objeto ou Dict de forma segura."""
        if obj is None:
            return default
        if isinstance(obj, dict):
            return obj.get(key, default)
        return getattr(obj, key, default)

    def _setup_ui(self):
        card = tk.Frame(self, bg=Config.COLOR_WHITE, padx=40, pady=30)
        card.place(relx=0.5, rely=0.5, anchor="center")

        titulo_texto = "Editar Produto" if self.produto else "Novo Produto"
        tk.Label(
            card,
            text=titulo_texto,
            font=Config.FONT_HEADER,
            bg=Config.COLOR_WHITE,
            fg=Config.COLOR_PRIMARY,
        ).pack(pady=(0, 20))

        # Campos
        self.ent_nome = self._create_field(card, "Nome do Produto")
        self.ent_sku = self._create_field(card, "SKU (Código)")

        row = tk.Frame(card, bg=Config.COLOR_WHITE)
        row.pack(fill="x", pady=5)
        self.ent_preco = self._create_field(row, "Preço (R$)", side="left", width=18)
        self.ent_estoque = self._create_field(row, "Estoque", side="right", width=18)

        tk.Label(
            card, text="Categoria", bg=Config.COLOR_WHITE, font=Config.FONT_BODY
        ).pack(anchor="w")
        self.combo_categoria = ttk.Combobox(card, width=37, state="readonly")
        self.combo_categoria.pack(pady=(0, 10))

        # Descrição
        tk.Label(
            card,
            text="Descrição Detalhada",
            bg=Config.COLOR_WHITE,
            font=Config.FONT_BODY,
        ).pack(anchor="w")
        self.txt_descricao = tk.Text(
            card,
            height=4,
            width=37,
            font=Config.FONT_BODY,
            bg="#F8F9FA",
            relief="sunken",
            bd=1,
        )
        self.txt_descricao.pack(pady=(0, 15))

        # Imagem
        tk.Label(
            card, text="Imagem do Produto", bg=Config.COLOR_WHITE, font=Config.FONT_BODY
        ).pack(anchor="w")
        img_row = tk.Frame(card, bg=Config.COLOR_WHITE)
        img_row.pack(fill="x", pady=(0, 15))

        tk.Button(
            img_row,
            text="Selecionar Arquivo...",
            command=self._select_image,
            bg="#E0E0E0",
        ).pack(side="left")

        self.lbl_imagem = tk.Label(
            img_row, text="Nenhum arquivo", bg=Config.COLOR_WHITE, fg="gray"
        )
        self.lbl_imagem.pack(side="left", padx=10)

        # Botões
        btn_frame = tk.Frame(card, bg=Config.COLOR_WHITE)
        btn_frame.pack(pady=20, fill="x")

        tk.Button(
            btn_frame,
            text="Cancelar",
            bg=Config.COLOR_SECONDARY,
            fg="white",
            width=12,
            command=lambda: self.controller.show_view(
                "ManageProducts", data=self.usuario
            ),
        ).pack(side="left")

        tk.Button(
            btn_frame,
            text="Salvar",
            bg=Config.COLOR_PRIMARY,
            fg="white",
            width=12,
            command=self._handle_save,
        ).pack(side="right")

    def _create_field(self, parent, label, side=None, width=40):
        container = tk.Frame(parent, bg=Config.COLOR_WHITE)
        if side:
            container.pack(side=side, expand=True, fill="x")
        else:
            container.pack(fill="x")

        tk.Label(
            container, text=label, bg=Config.COLOR_WHITE, font=Config.FONT_BODY
        ).pack(anchor="w")
        entry = tk.Entry(container, width=width, font=Config.FONT_BODY, bg="#F8F9FA")
        entry.pack(pady=(0, 10), fill="x")
        return entry

    def _select_image(self):
        file_path = filedialog.askopenfilename(
            title="Selecione uma imagem",
            filetypes=[("Imagens", "*.jpg *.jpeg *.png *.webp")],
        )
        if file_path:
            self.imagem_path = file_path
            self.lbl_imagem.config(text=file_path.split("/")[-1], fg="black")

    def _load_categories(self):
        try:
            cats = self.service.listar_categorias()
            nomes = []
            self.categorias_map = {}

            for c in cats:
                # CORREÇÃO CRÍTICA: Verificação explícita de tipo para evitar erro de atributo
                if isinstance(c, dict):
                    nome = c["nome"]
                    c_id = c["id"]
                else:
                    nome = c.nome
                    c_id = c.id

                nomes.append(nome)
                self.categorias_map[nome] = c_id

            self.combo_categoria["values"] = nomes

            if self.produto:
                self._fill_form()
            elif nomes:
                self.combo_categoria.current(0)

        except Exception as e:
            traceback.print_exc()
            messagebox.showerror("Erro", f"Falha ao carregar categorias: {e}")

    def _fill_form(self):
        """Preenche campos na edição (Híbrido: Objeto/Dict)."""
        if not self.produto:
            return

        # Helper interno para encurtar chamadas
        def get_p(key, default=""):
            return self._get_val(self.produto, key, default)

        # Campos simples
        self.ent_nome.delete(0, tk.END)
        self.ent_nome.insert(0, get_p("nome"))
        self.ent_sku.delete(0, tk.END)
        self.ent_sku.insert(0, get_p("sku"))
        self.ent_preco.delete(0, tk.END)
        self.ent_preco.insert(0, f"{float(get_p('preco', 0)):.2f}")
        self.ent_estoque.delete(0, tk.END)
        self.ent_estoque.insert(0, str(get_p("estoque")))

        # Descrição
        desc = get_p("descricao", "")
        self.txt_descricao.insert("1.0", desc)

        # Categoria (Lógica robusta para Objeto aninhado ou Dict plano)
        cat = get_p("categoria")
        cat_nome = ""

        if cat:
            # Se for objeto Categoria
            if hasattr(cat, "nome"):
                cat_nome = cat.nome
            # Se for dict Categoria
            elif isinstance(cat, dict):
                cat_nome = cat.get("nome", "")

        # Fallback se vier achatado da view (ex: categoria_nome)
        if not cat_nome:
            cat_nome = get_p("categoria_nome", "")

        if cat_nome in self.categorias_map:
            self.combo_categoria.set(cat_nome)

        # Imagem
        if get_p("imagem_principal"):
            self.lbl_imagem.config(
                text="Imagem Atual Mantida (selecione para trocar)", fg="blue"
            )

    def _handle_save(self):
        try:
            nome = self.ent_nome.get()
            sku = self.ent_sku.get()
            preco = self.ent_preco.get()
            estoque = self.ent_estoque.get()
            cat_nome = self.combo_categoria.get()

            descricao = self.txt_descricao.get("1.0", "end-1c").strip()

            if not cat_nome or cat_nome not in self.categorias_map:
                raise ValueError("Selecione uma categoria válida.")

            # Recupera ID da categoria
            cat_id = self.categorias_map[
                cat_nome
            ]  # Envia o ID para o service (opcional, pois service busca por nome)

            if self.produto:
                # Pega ID do objeto ou dict
                prod_id = self._get_val(self.produto, "id")

                self.service.atualizar_produto(
                    produto_id=prod_id,
                    nome=nome,
                    sku=sku,
                    preco=preco,
                    estoque=estoque,
                    nome_categoria=cat_nome,
                    descricao=descricao,
                    imagem_path=self.imagem_path,
                )
                messagebox.showinfo("Sucesso", "Produto atualizado!")
            else:
                self.service.cadastrar_produto(
                    nome=nome,
                    sku=sku,
                    preco=preco,
                    estoque=estoque,
                    nome_categoria=cat_nome,
                    descricao=descricao,
                    imagem_path=self.imagem_path,
                )
                messagebox.showinfo("Sucesso", "Produto cadastrado!")

            self.controller.show_view("ManageProducts", data=self.usuario)

        except ValueError as ve:
            messagebox.showwarning("Atenção", str(ve))
        except Exception as e:
            traceback.print_exc()
            messagebox.showerror("Erro Crítico", f"Não foi possível salvar: {e}")
