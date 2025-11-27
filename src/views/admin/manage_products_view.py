import tkinter as tk
from tkinter import ttk, messagebox
from src.config.settings import Config
from src.services.catalog_service import CatalogService

class ManageProductsView(tk.Frame):
    """
    Tela de Gestão de Produtos (CRUD).
    Exibe uma lista (Treeview) e botões de ação.
    """

    def __init__(self, parent, controller, data=None):
        super().__init__(parent, bg=Config.COLOR_BG)
        self.controller = controller
        self.service = CatalogService()
        
        self._setup_ui()
        # Carrega os dados logo após montar a tela
        self.after(100, self._load_data)

    def _setup_ui(self):
        # Cabeçalho
        header = tk.Frame(self, bg=Config.COLOR_WHITE, padx=20, pady=10)
        header.pack(fill="x")
        
        tk.Label(
            header, 
            text="Gerenciar Produtos", 
            font=Config.FONT_HEADER, 
            bg=Config.COLOR_WHITE, 
            fg=Config.COLOR_PRIMARY
        ).pack(side="left")

        # Botão Voltar
        tk.Button(
            header, 
            text="Voltar", 
            command=lambda: self.controller.show_view("AdminDashboard"),
            bg=Config.COLOR_BG
        ).pack(side="right")

        # Área Principal
        content = tk.Frame(self, bg=Config.COLOR_BG, padx=20, pady=20)
        content.pack(fill="both", expand=True)

        # Toolbar (Botões de Ação)
        toolbar = tk.Frame(content, bg=Config.COLOR_BG)
        toolbar.pack(fill="x", pady=(0, 10))

        tk.Button(
            toolbar, 
            text="+ Novo Produto", 
            bg=Config.COLOR_ACCENT, 
            fg="white",
            font=Config.FONT_SMALL,
            command=self._open_add_form
        ).pack(side="left", padx=5)

        tk.Button(
            toolbar, 
            text="🗑️ Excluir", 
            bg=Config.COLOR_SECONDARY, 
            fg="white",
            font=Config.FONT_SMALL,
            command=self._delete_selected
        ).pack(side="left", padx=5)

        # Tabela (Treeview)
        columns = ("id", "sku", "nome", "categoria", "preco", "estoque")
        self.tree = ttk.Treeview(content, columns=columns, show="headings", selectmode="browse")
        
        # Configurar Cabeçalhos
        self.tree.heading("id", text="ID")
        self.tree.heading("sku", text="SKU")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("categoria", text="Categoria")
        self.tree.heading("preco", text="Preço")
        self.tree.heading("estoque", text="Estoque")

        # Configurar Colunas
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("sku", width=100)
        self.tree.column("nome", width=300)
        self.tree.column("categoria", width=150)
        self.tree.column("preco", width=100, anchor="e")
        self.tree.column("estoque", width=80, anchor="center")

        # Scrollbar
        scrollbar = ttk.Scrollbar(content, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _load_data(self):
        """Busca dados do serviço e popula a tabela."""
        # Limpa dados antigos
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        try:
            produtos = self.service.listar_produtos()
            for p in produtos:
                # Trata a categoria (pode ser None ou Objeto)
                cat_nome = "-"
                if p.categoria:
                    cat_nome = p.categoria.nome
                
                self.tree.insert("", "end", values=(
                    p.id, 
                    p.sku, 
                    p.nome, 
                    cat_nome, 
                    f"R$ {p.preco:.2f}", 
                    p.estoque
                ))
        except Exception as e:
            print(f"Erro ao carregar: {e}")
            messagebox.showerror("Erro", f"Falha ao carregar produtos: {e}")

    def _open_add_form(self):
        """Navega para a tela de formulário."""
        self.controller.show_view("ProductFormView")

    def _delete_selected(self):
        """Remove o item selecionado."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Atenção", "Selecione um produto para excluir.")
            return
            
        item = self.tree.item(selected[0])
        prod_id = item['values'][0]
        
        if messagebox.askyesno("Confirmar", f"Deseja excluir o produto ID {prod_id}?"):
            try:
                self.service.remover_produto(prod_id)
                self._load_data() # Recarrega a tabela
                messagebox.showinfo("Sucesso", "Produto removido.")
            except Exception as e:
                messagebox.showerror("Erro", str(e))