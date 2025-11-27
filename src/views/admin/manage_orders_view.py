import tkinter as tk
from tkinter import ttk, messagebox
from src.config.settings import Config
from src.services.catalog_service import CatalogService

class ManageProductsView(tk.Frame):
    def __init__(self, parent, controller, data=None):
        super().__init__(parent, bg=Config.COLOR_BG)
        self.controller = controller
        self.service = CatalogService()
        
        self._setup_ui()
        self._load_data()

    def _setup_ui(self):
        # --- Cabeçalho ---
        header = tk.Frame(self, bg=Config.COLOR_WHITE, padx=20, pady=15)
        header.pack(fill="x")
        
        tk.Label(header, text="Gerenciar Produtos", font=Config.FONT_HEADER, 
                 bg=Config.COLOR_WHITE, fg=Config.COLOR_PRIMARY).pack(side="left")
        
        tk.Button(header, text="Voltar", bg=Config.COLOR_BG, fg=Config.COLOR_TEXT,
                  command=lambda: self.controller.show_view("AdminDashboard")).pack(side="right")

        # --- Área de Conteúdo ---
        content = tk.Frame(self, bg=Config.COLOR_BG, padx=20, pady=20)
        content.pack(fill="both", expand=True)

        # --- Toolbar ---
        toolbar = tk.Frame(content, bg=Config.COLOR_BG)
        toolbar.pack(fill="x", pady=(0, 10))

        # Botão Adicionar
        tk.Button(toolbar, text="+ Novo Produto", bg=Config.COLOR_ACCENT, fg="white",
                  font=Config.FONT_SMALL, width=15,
                  command=lambda: self.controller.show_view("ProductFormView")).pack(side="left", padx=5)

        # Botão Excluir
        tk.Button(toolbar, text="🗑️ Excluir Selecionado", bg=Config.COLOR_SECONDARY, fg="white",
                  font=Config.FONT_SMALL, width=20,
                  command=self._delete_product).pack(side="left", padx=5)

        # --- Tabela (Treeview) ---
        cols = ("ID", "SKU", "Nome", "Categoria", "Preço", "Estoque")
        self.tree = ttk.Treeview(content, columns=cols, show="headings", selectmode="browse")
        
        # Cabeçalhos
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        self.tree.column("Nome", width=300) # Nome mais largo
        
        self.tree.pack(fill="both", expand=True)

    def _load_data(self):
        # Limpa a tabela
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Busca do banco via serviço
        try:
            produtos = self.service.listar_produtos()
            for p in produtos:
                cat_nome = p.categoria.nome if p.categoria else "-"
                self.tree.insert("", "end", values=(
                    p.id, p.sku, p.nome, cat_nome, f"R$ {p.preco:.2f}", p.estoque
                ))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar produtos: {e}")

    def _delete_product(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Atenção", "Selecione um item para excluir.")
            return
            
        item = self.tree.item(selected[0])
        prod_id = item['values'][0] # Pega o ID da primeira coluna
        
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este produto?"):
            self.service.remover_produto(prod_id)
            self._load_data() # Atualiza a lista
            messagebox.showinfo("Sucesso", "Produto removido.")