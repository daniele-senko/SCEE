import tkinter as tk
from PIL import Image, ImageTk
import os
from src.config.settings import Config
from src.views.components.custom_button import CustomButton


class ProductDetailsModal(tk.Toplevel):
    """
    Modal de Detalhes do Produto (Design Clean).
    """

    def __init__(self, parent, produto, on_add_to_cart=None):
        super().__init__(parent)
        self.produto = produto
        self.on_add_to_cart = on_add_to_cart

        self.title(f"Detalhes: {self._get_val('nome')}")
        self.geometry("800x600")  # Janela maior para respirar
        self.configure(bg=Config.COLOR_BG)
        self.resizable(False, False)

        # Modal
        self.transient(parent)
        self.grab_set()

        self._build_ui()
        self._center_window(parent)

    def _get_val(self, key, default=None):
        if isinstance(self.produto, dict):
            return self.produto.get(key, default)
        return getattr(self.produto, key, default)

    def _center_window(self, parent):
        self.update_idletasks()
        try:
            x = parent.winfo_rootx() + (parent.winfo_width() // 2) - (800 // 2)
            y = parent.winfo_rooty() + (parent.winfo_height() // 2) - (600 // 2)
            self.geometry(f"+{x}+{y}")
        except:
            pass

    def _build_ui(self):
        # Card Principal (Fundo Branco com sombra simulada)
        main_card = tk.Frame(
            self, bg=Config.COLOR_WHITE, padx=30, pady=30, relief="solid", bd=1
        )
        main_card.pack(fill="both", expand=True, padx=40, pady=40)

        # --- COLUNA ESQUERDA: IMAGEM ---
        left_col = tk.Frame(main_card, bg=Config.COLOR_WHITE, width=350)
        left_col.pack(side="left", fill="y", padx=(0, 30))
        left_col.pack_propagate(False)

        self._load_image(left_col)

        # --- COLUNA DIREITA: INFO ---
        right_col = tk.Frame(main_card, bg=Config.COLOR_WHITE)
        right_col.pack(side="left", fill="both", expand=True)

        # 1. Categoria (Tag)
        cat = self._get_val("categoria")
        cat_nome = (
            cat.nome
            if hasattr(cat, "nome")
            else self.produto.get("categoria_nome", "Geral")
        )

        tk.Label(
            right_col,
            text=str(cat_nome).upper(),
            font=("TkDefaultFont", 9, "bold"),
            bg="#EEF2FF",  # Fundo azulzinho claro
            fg=Config.COLOR_ACCENT,
            padx=8,
            pady=2,
        ).pack(anchor="w", pady=(0, 15))

        # 2. Título
        tk.Label(
            right_col,
            text=self._get_val("nome"),
            font=("TkDefaultFont", 20, "bold"),
            bg=Config.COLOR_WHITE,
            fg=Config.COLOR_TEXT,
            wraplength=350,
            justify="left",
        ).pack(anchor="w")

        # 3. Código SKU (Cinza)
        sku = self._get_val("sku", "-")
        tk.Label(
            right_col,
            text=f"Cód: {sku}",
            font=Config.FONT_SMALL,
            bg=Config.COLOR_WHITE,
            fg=Config.COLOR_TEXT_LIGHT,
        ).pack(anchor="w", pady=(5, 20))

        # 4. Preço (Grande e Destaque)
        preco = self._get_val("preco", 0.0)
        tk.Label(
            right_col,
            text=f"R$ {preco:.2f}",
            font=("TkDefaultFont", 28, "bold"),
            bg=Config.COLOR_WHITE,
            fg=Config.COLOR_PRIMARY,
        ).pack(anchor="w")

        # 5. Descrição
        tk.Label(
            right_col,
            text="Sobre este produto:",
            font=("TkDefaultFont", 10, "bold"),
            bg=Config.COLOR_WHITE,
        ).pack(anchor="w", pady=(20, 5))

        desc_frame = tk.Frame(right_col, bg="#F9FAFB", padx=10, pady=10)
        desc_frame.pack(fill="x")

        desc_text = tk.Text(
            desc_frame,
            height=5,
            bg="#F9FAFB",
            relief="flat",
            font=Config.FONT_BODY,
            wrap="word",
            fg="#4B5563",
        )
        desc_text.insert("1.0", self._get_val("descricao", "Sem descrição detalhada."))
        desc_text.config(state="disabled")
        desc_text.pack(fill="both")

        # 6. Botões de Ação (Rodapé)
        btn_frame = tk.Frame(right_col, bg=Config.COLOR_WHITE)
        btn_frame.pack(side="bottom", fill="x", pady=(20, 0))

        # Botão Comprar Grande
        tk.Button(
            btn_frame,
            text="ADICIONAR AO CARRINHO",
            bg=Config.COLOR_ACCENT,
            fg="white",
            font=("TkDefaultFont", 11, "bold"),
            relief="flat",
            cursor="hand2",
            pady=12,
            command=self._add_cart_action,
        ).pack(fill="x", pady=(0, 10))

        # Botão Fechar (Texto simples)
        tk.Button(
            btn_frame,
            text="Continuar Comprando",
            bg=Config.COLOR_WHITE,
            fg=Config.COLOR_TEXT_LIGHT,
            font=Config.FONT_BODY,
            relief="flat",
            cursor="hand2",
            command=self.destroy,
        ).pack()

    def _add_cart_action(self):
        if self.on_add_to_cart:
            self.on_add_to_cart(self.produto)
            self.destroy()

    def _load_image(self, parent):
        try:
            path = None
            img_p = self._get_val("imagem_principal")
            imgs = self._get_val("imagens", [])
            if img_p:
                path = img_p
            elif imgs:
                path = imgs[0]

            if path:
                if not os.path.isabs(path):
                    path = os.path.join(Config.BASE_DIR, path)
                if os.path.exists(path):
                    img = Image.open(path)
                    img.thumbnail((350, 350))  # Imagem bem grande
                    self.photo = ImageTk.PhotoImage(img)
                    tk.Label(parent, image=self.photo, bg=Config.COLOR_WHITE).pack(
                        expand=True
                    )
                    return

            tk.Label(parent, text="Sem Imagem", bg="#F3F4F6", fg="#9CA3AF").pack(
                expand=True, fill="both"
            )
        except Exception:
            tk.Label(parent, text="Erro Imagem", bg="#FEE2E2").pack(
                expand=True, fill="both"
            )
