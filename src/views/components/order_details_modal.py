import tkinter as tk
from tkinter import ttk
from src.config.settings import Config
from src.views.components.custom_button import CustomButton


class OrderDetailsModal(tk.Toplevel):
    """
    Modal para exibir os detalhes completos de um pedido (Itens e Endereço).
    """

    def __init__(self, parent, pedido):
        super().__init__(parent)
        self.pedido = pedido

        self.title(f"Detalhes do Pedido #{pedido['id']}")
        self.geometry("600x500")
        self.configure(bg=Config.COLOR_BG)
        self.resizable(False, False)

        # Centraliza
        self.transient(parent)
        self.grab_set()

        self._build_ui()

        # Centraliza na tela
        self.update_idletasks()
        x = parent.winfo_rootx() + (parent.winfo_width() // 2) - (600 // 2)
        y = parent.winfo_rooty() + (parent.winfo_height() // 2) - (500 // 2)
        self.geometry(f"+{x}+{y}")

    def _build_ui(self):
        # Cabeçalho
        header = tk.Frame(self, bg=Config.COLOR_WHITE, padx=20, pady=15)
        header.pack(fill="x")

        tk.Label(
            header,
            text=f"Pedido #{self.pedido['id']} - {self.pedido['status']}",
            font=Config.FONT_HEADER,
            bg=Config.COLOR_WHITE,
            fg=Config.COLOR_PRIMARY,
        ).pack(anchor="w")

        tk.Label(
            header,
            text=f"Data: {self.pedido.get('criado_em', 'N/A')}",
            font=Config.FONT_SMALL,
            bg=Config.COLOR_WHITE,
            fg=Config.COLOR_TEXT_LIGHT,
        ).pack(anchor="w")

        # Corpo com Scroll
        content = tk.Frame(self, bg=Config.COLOR_BG, padx=20, pady=20)
        content.pack(fill="both", expand=True)

        # Seção 1: Itens
        tk.Label(
            content, text="Itens do Pedido", font=Config.FONT_BOLD, bg=Config.COLOR_BG
        ).pack(anchor="w", pady=(0, 5))

        tree_frame = tk.Frame(content)
        tree_frame.pack(fill="both", expand=True, pady=(0, 15))

        cols = ("Produto", "Qtd", "Unitário", "Total")
        tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=8)

        tree.heading("Produto", text="Produto")
        tree.column("Produto", width=250)
        tree.heading("Qtd", text="Qtd")
        tree.column("Qtd", width=50, anchor="center")
        tree.heading("Unitário", text="Unit.")
        tree.column("Unitário", width=80, anchor="e")
        tree.heading("Total", text="Total")
        tree.column("Total", width=80, anchor="e")

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Preenche Itens
        for item in self.pedido.get("itens", []):
            total_item = item["quantidade"] * item["preco_unitario"]
            tree.insert(
                "",
                "end",
                values=(
                    item["nome_produto"],
                    item["quantidade"],
                    f"R$ {item['preco_unitario']:.2f}",
                    f"R$ {total_item:.2f}",
                ),
            )

        # Seção 2: Totais e Endereço
        info_frame = tk.Frame(content, bg=Config.COLOR_WHITE, padx=15, pady=15)
        info_frame.pack(fill="x")

        # Totais (Direita)
        totals_frame = tk.Frame(info_frame, bg=Config.COLOR_WHITE)
        totals_frame.pack(side="right", anchor="n")

        subtotal = self.pedido.get("subtotal", 0.0)
        frete = self.pedido.get("frete", 0.0)
        total = self.pedido.get("total", 0.0)

        self._add_summary_row(totals_frame, "Subtotal:", subtotal)
        self._add_summary_row(totals_frame, "Frete:", frete)
        tk.Frame(totals_frame, height=1, bg="#CCC").pack(fill="x", pady=5)
        self._add_summary_row(totals_frame, "TOTAL:", total, is_bold=True)

        # Endereço (Esquerda)
        addr_frame = tk.Frame(info_frame, bg=Config.COLOR_WHITE)
        addr_frame.pack(side="left", anchor="n", fill="x", expand=True)

        end = self.pedido.get("endereco")
        if end:
            txt_end = (
                f"{end.get('logradouro')}, {end.get('numero')}\n"
                f"{end.get('bairro')} - {end.get('cidade')}/{end.get('estado')}\n"
                f"CEP: {end.get('cep')}"
            )
        else:
            txt_end = "Endereço não disponível."

        tk.Label(
            addr_frame,
            text="Endereço de Entrega:",
            font=Config.FONT_BOLD,
            bg=Config.COLOR_WHITE,
        ).pack(anchor="w")
        tk.Label(
            addr_frame,
            text=txt_end,
            font=Config.FONT_SMALL,
            bg=Config.COLOR_WHITE,
            justify="left",
        ).pack(anchor="w")

        # Botão Fechar
        CustomButton(
            self, text="Fechar", command=self.destroy, variant="secondary"
        ).pack(pady=10)

    def _add_summary_row(self, parent, label, value, is_bold=False):
        f = tk.Frame(parent, bg=Config.COLOR_WHITE)
        f.pack(fill="x")
        font = Config.FONT_BOLD if is_bold else Config.FONT_BODY
        tk.Label(f, text=label, font=font, bg=Config.COLOR_WHITE).pack(
            side="left", padx=(0, 10)
        )
        tk.Label(f, text=f"R$ {value:.2f}", font=font, bg=Config.COLOR_WHITE).pack(
            side="right"
        )
