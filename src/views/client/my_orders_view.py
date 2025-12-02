import tkinter as tk
from tkinter import ttk, messagebox
from src.config.settings import Config
from src.controllers.order_controller import OrderController
from src.views.components.order_details_modal import OrderDetailsModal

class MyOrdersView(tk.Frame):

    def __init__(self, parent, controller, data=None):
        super().__init__(parent, bg=Config.COLOR_BG)
        self.controller = controller

        if isinstance(data, dict) and "usuario" in data:
            self.usuario = data["usuario"]
        else:
            self.usuario = data

        self.order_controller = OrderController(controller)
        if self.usuario:
            self.order_controller.set_current_user(self.usuario.id)

        self._setup_ui()
        self.after(100, self._load_data)

    def _setup_ui(self):
        header = tk.Frame(self, bg=Config.COLOR_WHITE, padx=20, pady=15)
        header.pack(fill="x")

        tk.Label(
            header,
            text="Meus Pedidos",
            font=Config.FONT_HEADER,
            bg=Config.COLOR_WHITE,
            fg=Config.COLOR_PRIMARY,
        ).pack(side="left")

        tk.Button(
            header,
            text="Voltar para Loja",
            bg=Config.COLOR_BG,
            fg=Config.COLOR_TEXT,
            command=lambda: self.controller.show_view("HomeView", data=self.usuario),
        ).pack(side="right")

        content = tk.Frame(self, bg=Config.COLOR_BG, padx=20, pady=20)
        content.pack(fill="both", expand=True)

        cols = ("ID", "Data", "Status", "Total", "Itens")
        self.tree = ttk.Treeview(
            content, columns=cols, show="headings", selectmode="browse"
        )

        self.tree.heading("ID", text="Nº")
        self.tree.column("ID", width=60, anchor="center")
        self.tree.heading("Data", text="Data")
        self.tree.column("Data", width=120, anchor="center")
        self.tree.heading("Status", text="Status")
        self.tree.column("Status", width=120, anchor="center")
        self.tree.heading("Total", text="Total")
        self.tree.column("Total", width=100, anchor="e")
        self.tree.heading("Itens", text="Itens")
        self.tree.column("Itens", width=60, anchor="center")

        scrollbar = ttk.Scrollbar(content, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind de Duplo Clique
        self.tree.bind("<Double-1>", self._on_double_click)

        tk.Label(
            content,
            text="* Dê um duplo clique para ver detalhes ou cancelar",
            bg=Config.COLOR_BG,
            fg="gray",
        ).pack(anchor="w", pady=5)

    def _load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            resultado = self.order_controller.list_my_orders()
            if resultado["success"]:
                pedidos = resultado.get("data", [])
                if not pedidos:
                    return

                for pedido in pedidos:
                    data_str = str(pedido.get("criado_em", "N/A"))
                    total_val = pedido.get("total", 0.0)
                    itens = pedido.get("itens", [])
                    qtd_itens = len(itens) if isinstance(itens, list) else "-"

                    self.tree.insert(
                        "",
                        "end",
                        values=(
                            pedido.get("id"),
                            data_str,
                            pedido.get("status", "DESCONHECIDO"),
                            f"R$ {float(total_val):.2f}",
                            qtd_itens,
                        ),
                    )
            else:
                messagebox.showerror("Erro", resultado["message"])
        except Exception as e:
            print(f"Erro MyOrders: {e}")

    def _on_double_click(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        item = self.tree.item(selected[0])
        pedido_id = item["values"][0]

        # Busca detalhes completos via controller
        res = self.order_controller.get_order_details(pedido_id)

        if res["success"]:
            # Abre modal passando callback para recarregar a tabela se cancelar
            OrderDetailsModal(
                self,
                res["data"],
                self.order_controller,
                on_close_callback=self._load_data,
            )
        else:
            messagebox.showerror("Erro", res["message"])
