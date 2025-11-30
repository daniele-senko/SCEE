import tkinter as tk
from tkinter import ttk, messagebox
from src.config.settings import Config
from src.controllers.admin_controller import AdminController


class ManageOrdersView(tk.Frame):
    """
    Tela de Gestão de Pedidos para Admin.
    Exibe todos os pedidos do sistema.
    """
    
    def __init__(self, parent, controller, data=None):
        super().__init__(parent, bg=Config.COLOR_BG)
        self.controller = controller
        self.usuario = data  # Guarda o usuário logado
        self.admin_controller = AdminController(controller)
        
        # Define o admin atual no controller
        if self.usuario and hasattr(self.usuario, 'id'):
            self.admin_controller.set_current_admin(self.usuario.id)
        
        self._setup_ui()
        self._load_data()

    def _setup_ui(self):
        # Cabeçalho
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

        # Área de Conteúdo
        content = tk.Frame(self, bg=Config.COLOR_BG, padx=20, pady=20)
        content.pack(fill="both", expand=True)

        # Tabela (Treeview)
        cols = ("ID", "Cliente", "Data", "Status", "Total", "Itens")
        self.tree = ttk.Treeview(content, columns=cols, show="headings", selectmode="browse")
        
        # Cabeçalhos
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        
        self.tree.column("Cliente", width=200)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(content, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _load_data(self):
        """Carrega todos os pedidos do sistema."""
        # Limpa a tabela
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        try:
            resultado = self.admin_controller.list_all_orders()
            
            if resultado['success']:
                pedidos = resultado.get('data', [])
                
                for pedido in pedidos:
                    cliente_nome = pedido.get('cliente_nome', 'N/A')
                    data = pedido.get('created_at', 'N/A')
                    status = pedido.get('status', 'N/A')
                    total = pedido.get('total', 0.0)
                    qtd_itens = len(pedido.get('itens', []))
                    
                    self.tree.insert("", "end", values=(
                        pedido.get('id'),
                        cliente_nome,
                        data,
                        status,
                        f"R$ {total:.2f}",
                        qtd_itens
                    ))
            else:
                messagebox.showerror("Erro", resultado['message'])
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar pedidos: {e}")