import tkinter as tk
from tkinter import ttk, messagebox
import traceback # Importante para ver erros detalhados no terminal
from src.config.settings import Config
from src.services.catalog_service import CatalogService

class ProductFormView(tk.Frame):
    """
    Formulário para Adicionar/Editar Produto.
    """

    def __init__(self, parent, controller, data=None):
        super().__init__(parent, bg=Config.COLOR_BG)
        self.controller = controller
        self.usuario = data  # Guarda o usuário logado
        self.service = CatalogService()
        self.categorias_map = {} # Dicionário para guardar {Nome: ID}
        
        self._setup_ui()
        # Carrega as categorias assim que a tela abre
        self.after(100, self._load_categories) 

    def _setup_ui(self):
        # Container Centralizado (Card Branco)
        card = tk.Frame(self, bg=Config.COLOR_WHITE, padx=40, pady=40)
        card.place(relx=0.5, rely=0.5, anchor="center")

        # Título
        tk.Label(
            card, 
            text="Novo Produto", 
            font=Config.FONT_HEADER, 
            bg=Config.COLOR_WHITE,
            fg=Config.COLOR_PRIMARY
        ).pack(pady=(0, 20))

        # Campos do Formulário
        self.ent_nome = self._create_field(card, "Nome do Produto")
        self.ent_sku = self._create_field(card, "SKU (Código)")
        
        # Frame para Preço e Estoque na mesma linha
        row = tk.Frame(card, bg=Config.COLOR_WHITE)
        row.pack(fill="x", pady=5)
        
        self.ent_preco = self._create_field(row, "Preço (R$)", side="left", width=18)
        self.ent_estoque = self._create_field(row, "Estoque", side="right", width=18)

        # --- Combobox de Categoria ---
        tk.Label(card, text="Categoria", bg=Config.COLOR_WHITE, font=Config.FONT_BODY).pack(anchor="w")
        
        self.combo_categoria = ttk.Combobox(card, width=37, state="readonly")
        self.combo_categoria.pack(pady=(0, 15))

        # --- Botões ---
        btn_frame = tk.Frame(card, bg=Config.COLOR_WHITE)
        btn_frame.pack(pady=20, fill="x")

        # Botão Cancelar
        tk.Button(
            btn_frame, 
            text="Cancelar", 
            bg=Config.COLOR_SECONDARY, 
            fg="white",
            width=12,
            command=lambda: self.controller.show_view("ManageProducts", data=self.usuario)
        ).pack(side="left")

        # Botão Salvar
        tk.Button(
            btn_frame, 
            text="Salvar", 
            bg=Config.COLOR_PRIMARY, 
            fg="white",
            width=12,
            command=self._handle_save
        ).pack(side="right")

    def _create_field(self, parent, label, side=None, width=40):
        """Helper para criar label + entry padronizados."""
        container = tk.Frame(parent, bg=Config.COLOR_WHITE)
        if side:
            container.pack(side=side, expand=True, fill="x")
        else:
            container.pack(fill="x")
            
        tk.Label(container, text=label, bg=Config.COLOR_WHITE, font=Config.FONT_BODY).pack(anchor="w")
        entry = tk.Entry(container, width=width, font=Config.FONT_BODY, bg="#F8F9FA")
        entry.pack(pady=(0, 15), fill="x")
        return entry

    def _load_categories(self):
        """Carrega categorias do banco para o dropdown."""
        print("--- DEBUG: Iniciando carregamento de categorias na TELA ---")
        try:
            cats = self.service.listar_categorias()
            print(f"--- DEBUG: Serviço retornou {len(cats)} categorias ---")
            
            nomes = []
            self.categorias_map = {}
            
            for c in cats:
                # Debug para ver o que tem dentro de cada item
                # print(f"DEBUG ITEM: {c} (Tipo: {type(c)})")
                
                # Verifica se é Objeto ou Dict (para compatibilidade)
                if isinstance(c, dict):
                    nome = c['nome']
                    c_id = c['id']
                else:
                    nome = c.nome
                    c_id = c.id
                
                nomes.append(nome)
                self.categorias_map[nome] = c_id # Guarda o ID para usar no save
            
            print(f"--- DEBUG: Nomes carregados no Combo: {nomes}")
            self.combo_categoria['values'] = nomes
            
            if nomes:
                self.combo_categoria.current(0) # Seleciona o primeiro
                
        except Exception as e:
            print("❌ ERRO CRÍTICO AO CARREGAR CATEGORIAS:")
            traceback.print_exc() # Imprime o erro completo no terminal
            messagebox.showerror("Erro", f"Falha ao carregar categorias: {e}")

    def _handle_save(self):
        try:
            # Coleta dados da tela
            nome = self.ent_nome.get()
            sku = self.ent_sku.get()
            preco = self.ent_preco.get()
            estoque = self.ent_estoque.get()
            
            # Validação da Categoria
            cat_nome = self.combo_categoria.get()
            if not cat_nome or cat_nome not in self.categorias_map:
                raise ValueError("Selecione uma categoria válida.")
            
            # Recupera o ID da categoria pelo nome selecionado
            cat_id = self.categorias_map[cat_nome] # Só mandamos o nome para o service

            # Chama o Service
            # Note: O método cadastrar_produto do service espera 'nome_categoria'
            # Mas como temos o ID e o service faz a busca, vamos passar o nome mesmo
            self.service.cadastrar_produto(nome, sku, preco, estoque, cat_nome)
            
            messagebox.showinfo("Sucesso", "Produto cadastrado!")
            self.controller.show_view("ManageProducts", data=self.usuario)
            
        except ValueError as ve:
            messagebox.showwarning("Validação", str(ve))
        except Exception as e:
            print("❌ ERRO AO SALVAR:")
            traceback.print_exc()
            messagebox.showerror("Erro Crítico", f"Não foi possível salvar: {e}")