import tkinter as tk
from tkinter import ttk, messagebox
from src.config.settings import Config
from src.controllers.admin_controller import AdminController

class ManageOrdersView(tk.Frame):
    """
    Tela de Gestão de Pedidos para Admin.
    Exibe todos os pedidos e permite alterar o status.
    """
    
    def __init__(self, parent, controller, data=None):
        super().__init__(parent, bg=Config.COLOR_BG)
        self.controller = controller
        self.usuario = data  # Guarda o usuário logado
        
        # Instancia o controlador
        self.admin_controller = AdminController(controller)
        
        # Configura o ID do admin no controller
        if self.usuario and hasattr(self.usuario, 'id'):
            self.admin_controller.set_current_admin(self.usuario.id)
        
        self._setup_ui()
        # Carrega os dados após montar a tela
        self.after(100, self._load_data)

    def _setup_ui(self):
        """Constrói a interface gráfica."""
        
        # --- Cabeçalho ---
        header = tk.Frame(self, bg=Config.COLOR_WHITE, padx=20, pady=15)
        header.pack(fill="x")
        
        tk.Label(
            header, 
            text="Gerenciar Pedidos", 
            font=Config.FONT_HEADER, 
            bg=Config.COLOR_WHITE, 
            fg=Config.COLOR_PRIMARY
        ).pack(side="left")
        
        tk.Button(
            header, 
            text="Voltar", 
            bg=Config.COLOR_BG, 
            fg=Config.COLOR_TEXT,
            command=lambda: self.controller.show_view("AdminDashboard", data=self.usuario)
        ).pack(side="right")

        # --- Tabela de Pedidos ---
        content = tk.Frame(self, bg=Config.COLOR_BG, padx=20, pady=20)
        content.pack(fill="both", expand=True)

        cols = ("ID", "Cliente", "Data", "Status", "Total", "Itens")
        self.tree = ttk.Treeview(content, columns=cols, show="headings", selectmode="browse")
        
        # Configuração das Colunas
        self.tree.heading("ID", text="ID")
        self.tree.column("ID", width=50, anchor="center")
        
        self.tree.heading("Cliente", text="Cliente")
        self.tree.column("Cliente", width=200, anchor="w")
        
        self.tree.heading("Data", text="Data")
        self.tree.column("Data", width=120, anchor="center")
        
        self.tree.heading("Status", text="Status")
        self.tree.column("Status", width=100, anchor="center")
        
        self.tree.heading("Total", text="Total")
        self.tree.column("Total", width=100, anchor="e") # Alinhado à direita
        
        self.tree.heading("Itens", text="Itens")
        self.tree.column("Itens", width=50, anchor="center")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(content, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # --- Barra de Ações (Alterar Status) ---
        action_frame = tk.Frame(self, bg=Config.COLOR_WHITE, padx=20, pady=15)
        action_frame.pack(fill="x", side="bottom")
        
        tk.Label(
            action_frame, 
            text="Alterar Status para:", 
            bg=Config.COLOR_WHITE, 
            font=Config.FONT_BODY
        ).pack(side="left", padx=(0, 10))
        
        self.combo_status = ttk.Combobox(
            action_frame, 
            values=["PENDENTE", "PROCESSANDO", "ENVIADO", "ENTREGUE", "CANCELADO"],
            state="readonly",
            width=20
        )
        self.combo_status.pack(side="left", padx=10)
        self.combo_status.current(1) # Padrão: PROCESSANDO
        
        tk.Button(
            action_frame,
            text="Atualizar Status",
            bg=Config.COLOR_PRIMARY,
            fg="white",
            font=Config.FONT_HEADER, 
            command=self._handle_update_status
        ).pack(side="left")

    def _load_data(self):
        """Busca os dados e preenche a tabela."""
        # Limpa tabela atual
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        try:
            resultado = self.admin_controller.list_all_orders()
            
            if resultado['success']:
                pedidos = resultado.get('data', [])
                
                if not pedidos:
                    # Se não houver pedidos, não faz nada (tabela fica vazia)
                    return

                for pedido in pedidos:
                    # Tenta pegar a data com diferentes chaves possíveis (compatibilidade)
                    data_str = pedido.get('data_pedido') or pedido.get('created_at') or 'N/A'
                    
                    self.tree.insert("", "end", values=(
                        pedido.get('id'),
                        pedido.get('cliente_nome', 'Cliente Desconhecido'),
                        data_str,
                        pedido.get('status', 'N/A'),
                        f"R$ {pedido.get('total', 0.0):.2f}",
                        len(pedido.get('itens', []))
                    ))
            else:
                messagebox.showerror("Erro", f"Erro ao buscar pedidos: {resultado['message']}")
                
        except Exception as e:
            print(f"Erro detalhado ManageOrders: {e}")
            messagebox.showerror("Erro Crítico", "Falha ao carregar lista de pedidos.")

    def _handle_update_status(self):
        """Processa a alteração de status."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um pedido na tabela.")
            return
            
        # Pega o ID da linha selecionada
        item = self.tree.item(selected[0])
        pedido_id = item['values'][0]
        novo_status = self.combo_status.get()
        
        if messagebox.askyesno("Confirmar", f"Mudar pedido #{pedido_id} para {novo_status}?"):
            try:
                res = self.admin_controller.update_order_status(pedido_id, novo_status)
                if res['success']:
                    messagebox.showinfo("Sucesso", "Status atualizado!")
                    self._load_data() # Recarrega a tabela
                else:
                    messagebox.showerror("Erro", res['message'])
            except Exception as e:
                messagebox.showerror("Erro", f"Falha na atualização: {e}")