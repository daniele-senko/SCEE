import tkinter as tk
from tkinter import ttk
from src.config.settings import Config
from src.views.components.custom_button import CustomButton
from src.views.components.modal_message import show_success, show_error, show_confirm


class OrderDetailsModal(tk.Toplevel):
    """
    Modal para exibir os detalhes completos de um pedido e permitir cancelamento.
    """

    def __init__(self, parent, pedido, controller=None, on_close_callback=None):
        super().__init__(parent)
        self.pedido = pedido
        self.controller = controller
        self.on_close_callback = on_close_callback

        # Fonte negrito local (já que Config não tem FONT_BOLD)
        self.FONT_BOLD = ("TkDefaultFont", 10, "bold")

        self.title(f"Detalhes do Pedido #{pedido['id']}")
        self.geometry("650x600")
        self.configure(bg=Config.COLOR_BG)
        self.resizable(False, False)

        # Modal setup
        self.transient(parent)
        self.grab_set()

        self._build_ui()

        # Centraliza
        self.update_idletasks()
        try:
            x = parent.winfo_rootx() + (parent.winfo_width() // 2) - (650 // 2)
            y = parent.winfo_rooty() + (parent.winfo_height() // 2) - (600 // 2)
            self.geometry(f"+{x}+{y}")
        except:
            pass

    def _build_ui(self):
        # --- Cabeçalho ---
        header = tk.Frame(self, bg=Config.COLOR_WHITE, padx=20, pady=15)
        header.pack(fill="x")

        status = self.pedido.get("status", "N/A")
        tk.Label(
            header,
            text=f"Pedido #{self.pedido['id']} - {status}",
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

        # --- Conteúdo ---
        content = tk.Frame(self, bg=Config.COLOR_BG, padx=20, pady=20)
        content.pack(fill="both", expand=True)

        # Tabela de Itens
        tk.Label(
            content, text="Itens do Pedido", font=self.FONT_BOLD, bg=Config.COLOR_BG
        ).pack(anchor="w", pady=(0, 5))

        tree_frame = tk.Frame(content)
        tree_frame.pack(fill="both", expand=True, pady=(0, 15))

        cols = ("Produto", "Qtd", "Unitário", "Total")
        tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=6)

        tree.heading("Produto", text="Produto")
        tree.column("Produto", width=220)
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
            # Garante numérico
            qtd = float(item.get("quantidade", 0))
            preco = float(item.get("preco_unitario", 0))
            total_item = qtd * preco

            tree.insert(
                "",
                "end",
                values=(
                    item.get("nome_produto", "Produto"),
                    int(qtd),
                    f"R$ {preco:.2f}",
                    f"R$ {total_item:.2f}",
                ),
            )

        # --- Resumo e Endereço ---
        info_frame = tk.Frame(content, bg=Config.COLOR_WHITE, padx=15, pady=15)
        info_frame.pack(fill="x")

        # Totais (Direita)
        totals_frame = tk.Frame(info_frame, bg=Config.COLOR_WHITE)
        totals_frame.pack(side="right", anchor="n")

        subtotal = float(self.pedido.get("subtotal", 0.0))
        frete = float(self.pedido.get("frete", 0.0))
        total = float(self.pedido.get("total", 0.0))

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
            font=self.FONT_BOLD,
            bg=Config.COLOR_WHITE,
        ).pack(anchor="w")
        tk.Label(
            addr_frame,
            text=txt_end,
            font=Config.FONT_SMALL,
            bg=Config.COLOR_WHITE,
            justify="left",
        ).pack(anchor="w")

        # --- Botões de Ação ---
        btn_frame = tk.Frame(content, bg=Config.COLOR_BG, pady=10)
        btn_frame.pack(fill="x", side="bottom")

        # Botão Fechar
        CustomButton(
            btn_frame, text="Fechar", command=self.destroy, variant="secondary"
        ).pack(side="right")

        # Botão Cancelar
        if self.pedido.get("pode_cancelar", False) and self.controller:
            CustomButton(
                btn_frame,
                text="Cancelar Pedido",
                command=self._cancelar_pedido,
                variant="secondary",
                bg="#DC2626",
            ).pack(side="left")

    def _add_summary_row(self, parent, label, value, is_bold=False):
        f = tk.Frame(parent, bg=Config.COLOR_WHITE)
        f.pack(fill="x")
        font = self.FONT_BOLD if is_bold else Config.FONT_BODY
        tk.Label(f, text=label, font=font, bg=Config.COLOR_WHITE).pack(
            side="left", padx=(0, 10)
        )
        tk.Label(f, text=f"R$ {value:.2f}", font=font, bg=Config.COLOR_WHITE).pack(
            side="right"
        )

    def _cancelar_pedido(self):
        """Lógica para cancelar o pedido."""
        if show_confirm(
            self,
            "Cancelar Pedido",
            "Tem certeza que deseja cancelar este pedido?\nO estoque será reposto.",
        ):
            if not self.controller:
                return

            res = self.controller.cancel_order(self.pedido["id"])

            if res["success"]:
                show_success(self, "Sucesso", res["message"])
                if self.on_close_callback:
                    self.on_close_callback()
                self.destroy()
            else:
                show_error(self, "Erro", res["message"])
