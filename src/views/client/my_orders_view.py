import tkinter as tk
from tkinter import ttk, messagebox
from src.config.settings import Config
from src.controllers.order_controller import OrderController
from src.views.components.order_details_modal import OrderDetailsModal


class MyOrdersView(tk.Frame):
    """
    Tela de 'Meus Pedidos' do Cliente.
    Exibe o histórico de compras.
    """

    def __init__(self, parent, controller, data=None):
        super().__init__(parent, bg=Config.COLOR_BG)
        self.controller = controller

        # Extrai o usuário do pacote de dados (se vier em dict)
        if isinstance(data, dict) and "usuario" in data:
            self.usuario = data["usuario"]
        else:
            self.usuario = data

        self.order_controller = OrderController(controller)

        if self.usuario:
            self.order_controller.set_current_user(self.usuario.id)

        self._setup_ui()
        # Carrega dados após montar a tela
        self.after(100, self._load_data)

    def _setup_ui(self):
        # Cabeçalho
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

        # Área de Conteúdo
        content = tk.Frame(self, bg=Config.COLOR_BG, padx=20, pady=20)
        content.pack(fill="both", expand=True)

        # Tabela
        cols = ("ID", "Data", "Status", "Total", "Itens")
        self.tree = ttk.Treeview(
            content, columns=cols, show="headings", selectmode="browse"
        )

        self.tree.heading("ID", text="Nº Pedido")
        self.tree.column("ID", width=80, anchor="center")

        self.tree.heading("Data", text="Data")
        self.tree.column("Data", width=120, anchor="center")

        self.tree.heading("Status", text="Status")
        self.tree.column("Status", width=120, anchor="center")

        self.tree.heading("Total", text="Valor Total")
        self.tree.column("Total", width=100, anchor="e")

        self.tree.heading("Itens", text="Qtd Itens")
        self.tree.column("Itens", width=80, anchor="center")

        self.tree.bind("<Double-1>", self._on_double_click)

        scrollbar = ttk.Scrollbar(content, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _on_double_click(self, event):
        """Abre modal de detalhes ao clicar duas vezes."""
        selected = self.tree.selection()
        if not selected:
            return

        item = self.tree.item(selected[0])
        pedido_id = item["values"][0]

        # Busca detalhes completos
        res = self.order_controller.get_order_details(pedido_id)

        if res["success"]:
            OrderDetailsModal(self, res["data"])
        else:
            messagebox.showerror("Erro", res["message"])

    def _load_data(self):
        """Busca os pedidos e preenche a tabela."""
        # Limpa tabela
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            # Chama controller (retorna Dict com 'success' e 'data')
            resultado = self.order_controller.list_my_orders()

            if resultado["success"]:
                pedidos = resultado.get("data", [])

                if not pedidos:
                    return  # Tabela vazia

                for pedido in pedidos:
                    # CORREÇÃO AQUI: Acessando como Dicionário, não Objeto!
                    # O Repositório retorna dicts (ex: {'id': 1, 'total': 50.0...})

                    # Formata data
                    data_str = str(pedido.get("criado_em", "N/A"))

                    # Formata valores
                    total_val = pedido.get("total", 0.0)
                    if isinstance(total_val, (int, float)):
                        total_str = f"R$ {total_val:.2f}"
                    else:
                        total_str = str(total_val)

                    # Contagem de itens (se vier join ou lista)
                    # Se não vier, mostramos '-'
                    itens = pedido.get("itens", [])
                    qtd_itens = len(itens) if isinstance(itens, list) else "-"

                    self.tree.insert(
                        "",
                        "end",
                        values=(
                            pedido.get("id"),
                            data_str,
                            pedido.get("status", "DESCONHECIDO"),
                            total_str,
                            qtd_itens,
                        ),
                    )
            else:
                messagebox.showerror("Erro", resultado["message"])

        except Exception as e:
            print(f"Erro em MyOrdersView: {e}")
            messagebox.showerror("Erro", "Falha ao carregar seus pedidos.")
