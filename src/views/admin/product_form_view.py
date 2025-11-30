import tkinter as tk
from tkinter import ttk, messagebox, filedialog # 'filedialog' é usado para abrir a janela de seleção de arquivos
import traceback # Permite imprimir o "rastro" do erro (stack trace) no terminal para debug
from src.config.settings import Config
from src.services.catalog_service import CatalogService

class ProductFormView(tk.Frame):
    """
    Formulário para Adicionar ou Editar Produtos.
    
    ESTUDO: Esta classe representa a camada de VIEW (Apresentação).
    Ela não deve conter regras de negócio complexas (como salvar no banco ou validar CPF).
    Sua função é coletar dados do usuário e repassar para o SERVICE.
    """

    def __init__(self, parent, controller, data=None):
        # Chama o construtor da classe pai (tk.Frame) definindo a cor de fundo
        super().__init__(parent, bg=Config.COLOR_BG)
        
        # O 'controller' é usado para navegar entre telas (ex: voltar para a lista)
        self.controller = controller
        
        # Tratamento dos dados recebidos da tela anterior.
        # 'data' pode conter o usuário logado e, no caso de edição, o produto a ser editado.
        if isinstance(data, dict) and 'usuario' in data:
            self.usuario = data['usuario']
            self.produto = data.get('produto', None)  # Se for None, é um cadastro Novo. Se tiver objeto, é Edição.
        else:
            self.usuario = data
            self.produto = None
        
        # Instancia o Serviço de Catálogo.
        # ESTUDO: Aqui conectamos a View ao Service (Camada de Negócio).
        self.service = CatalogService()
        
        # Dicionário auxiliar para mapear "Nome da Categoria" -> "ID da Categoria"
        # Isso é necessário porque o Combobox mostra nomes, mas o banco precisa de IDs.
        self.categorias_map = {} 
        
        # Variável para armazenar o caminho da imagem selecionada pelo usuário (em disco)
        self.imagem_path = None
        
        # Monta a interface gráfica
        self._setup_ui()
        
        # Agenda o carregamento das categorias para 100ms após a tela abrir.
        # Isso evita travar a interface gráfica durante a renderização inicial.
        self.after(100, self._load_categories) 

    def _setup_ui(self):
        """Configura todos os widgets (botões, campos, labels) da tela."""
        
        # Cria um "Cartão" branco centralizado para agrupar os campos
        card = tk.Frame(self, bg=Config.COLOR_WHITE, padx=40, pady=40)
        card.place(relx=0.5, rely=0.5, anchor="center")

        # Define o título dinamicamente (Novo ou Editar)
        titulo_texto = "Editar Produto" if self.produto else "Novo Produto"
        tk.Label(
            card, 
            text=titulo_texto, 
            font=Config.FONT_HEADER, 
            bg=Config.COLOR_WHITE,
            fg=Config.COLOR_PRIMARY
        ).pack(pady=(0, 20))

        # --- Campos de Texto ---
        self.ent_nome = self._create_field(card, "Nome do Produto")
        self.ent_sku = self._create_field(card, "SKU (Código único)")
        
        # Frame auxiliar para colocar Preço e Estoque lado a lado
        row = tk.Frame(card, bg=Config.COLOR_WHITE)
        row.pack(fill="x", pady=5)
        
        self.ent_preco = self._create_field(row, "Preço (R$)", side="left", width=18)
        self.ent_estoque = self._create_field(row, "Estoque", side="right", width=18)

        # --- Combobox de Categoria ---
        tk.Label(card, text="Categoria", bg=Config.COLOR_WHITE, font=Config.FONT_BODY).pack(anchor="w")
        self.combo_categoria = ttk.Combobox(card, width=37, state="readonly")
        self.combo_categoria.pack(pady=(0, 15))

        # --- Seleção de Imagem ---
        tk.Label(card, text="Imagem do Produto", bg=Config.COLOR_WHITE, font=Config.FONT_BODY).pack(anchor="w")
        
        # Frame para alinhar o botão e o texto do arquivo selecionado
        img_row = tk.Frame(card, bg=Config.COLOR_WHITE)
        img_row.pack(fill="x", pady=(0, 15))
        
        # Botão para abrir o explorador de arquivos
        tk.Button(
            img_row,
            text="Selecionar Arquivo...",
            command=self._select_image, # Chama a função de seleção
            bg="#E0E0E0"
        ).pack(side="left")
        
        # Label para mostrar qual arquivo foi escolhido (feedback para o usuário)
        self.lbl_imagem = tk.Label(img_row, text="Nenhum arquivo selecionado", bg=Config.COLOR_WHITE, fg="gray")
        self.lbl_imagem.pack(side="left", padx=10)

        # --- Botões de Ação ---
        btn_frame = tk.Frame(card, bg=Config.COLOR_WHITE)
        btn_frame.pack(pady=20, fill="x")

        # Botão Cancelar (Volta para a tela de listagem)
        tk.Button(
            btn_frame, 
            text="Cancelar", 
            bg=Config.COLOR_SECONDARY, 
            fg="white",
            width=12,
            command=lambda: self.controller.show_view("ManageProducts", data=self.usuario)
        ).pack(side="left")

        # Botão Salvar (Dispara a lógica de negócio)
        tk.Button(
            btn_frame, 
            text="Salvar", 
            bg=Config.COLOR_PRIMARY, 
            fg="white",
            width=12,
            command=self._handle_save
        ).pack(side="right")

    def _create_field(self, parent, label, side=None, width=40):
        """
        Método auxiliar (Helper) para criar pares de Label + Entry padronizados.
        Evita repetição de código na criação da UI.
        """
        container = tk.Frame(parent, bg=Config.COLOR_WHITE)
        if side:
            container.pack(side=side, expand=True, fill="x")
        else:
            container.pack(fill="x")
            
        tk.Label(container, text=label, bg=Config.COLOR_WHITE, font=Config.FONT_BODY).pack(anchor="w")
        entry = tk.Entry(container, width=width, font=Config.FONT_BODY, bg="#F8F9FA")
        entry.pack(pady=(0, 15), fill="x")
        return entry
    
    def _select_image(self):
        """
        Abre a janela nativa do sistema operacional para escolher uma imagem.
        """
        # Abre o dialog filtrando por arquivos de imagem
        file_path = filedialog.askopenfilename(
            title="Selecione uma imagem",
            filetypes=[("Imagens", "*.jpg *.jpeg *.png *.webp")]
        )
        
        # Se o usuário selecionou algo (não clicou em cancelar)
        if file_path:
            self.imagem_path = file_path # Guarda o caminho na variável da classe
            # Atualiza o texto visual para o usuário ver o que selecionou (só o nome do arquivo)
            nome_arquivo = file_path.split("/")[-1] 
            self.lbl_imagem.config(text=nome_arquivo, fg="black")

    def _load_categories(self):
        """Busca categorias no banco através do Service para preencher o Combobox."""
        try:
            cats = self.service.listar_categorias()
            
            nomes = []
            self.categorias_map = {} # Limpa o mapa
            
            for c in cats:
                # Tratamento para garantir compatibilidade se vier Dict ou Objeto
                if isinstance(c, dict):
                    nome = c['nome']
                    c_id = c['id']
                else:
                    nome = c.nome
                    c_id = c.id
                
                nomes.append(nome)
                self.categorias_map[nome] = c_id # Mapeia Nome -> ID
            
            self.combo_categoria['values'] = nomes
            
            # Se for edição, preenche os campos com os dados existentes
            if self.produto:
                self._fill_form()
            elif nomes:
                self.combo_categoria.current(0) # Seleciona o primeiro por padrão
                
        except Exception as e:
            traceback.print_exc()
            messagebox.showerror("Erro", f"Falha ao carregar categorias: {e}")
    
    def _fill_form(self):
        """Preenche o formulário com dados do produto (usado apenas na Edição)."""
        if not self.produto:
            return
        
        # Limpa e insere os dados
        self.ent_nome.delete(0, tk.END)
        self.ent_nome.insert(0, self.produto.nome)
        
        self.ent_sku.delete(0, tk.END)
        self.ent_sku.insert(0, self.produto.sku)
        
        self.ent_preco.delete(0, tk.END)
        self.ent_preco.insert(0, f"{self.produto.preco:.2f}")
        
        self.ent_estoque.delete(0, tk.END)
        self.ent_estoque.insert(0, str(self.produto.estoque))
        
        # Seleciona a categoria correta no Combobox
        if self.produto.categoria:
            # Verifica se category é objeto ou dict (robustez)
            cat_nome = self.produto.categoria.nome if hasattr(self.produto.categoria, 'nome') else self.produto.categoria.get('nome')
            
            if cat_nome in self.categorias_map:
                idx = list(self.categorias_map.keys()).index(cat_nome)
                self.combo_categoria.current(idx)

    def _handle_save(self):
        """
        Coleta os dados, valida e chama o Service para salvar.
        ESTUDO: A View captura eventos, mas quem EXECUTA a gravação é o Service.
        """
        try:
            # 1. Coleta dados (Getters dos widgets)
            nome = self.ent_nome.get()
            sku = self.ent_sku.get()
            preco = self.ent_preco.get()
            estoque = self.ent_estoque.get()
            cat_nome = self.combo_categoria.get()
            
            # 2. Validações básicas de UI
            if not cat_nome or cat_nome not in self.categorias_map:
                raise ValueError("Selecione uma categoria válida.")
            
            # 3. Chama o Service apropriado
            if self.produto:
                # EDITA um produto existente
                self.service.atualizar_produto(
                    produto_id=self.produto.id,
                    nome=nome,
                    sku=sku,
                    preco=preco,
                    estoque=estoque,
                    nome_categoria=cat_nome,
                    imagem_path=self.imagem_path # Passamos a imagem (pode ser None se não trocou)
                )
                messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
            else:
                # CRIA um novo produto
                self.service.cadastrar_produto(
                    nome=nome, 
                    sku=sku, 
                    preco=preco, 
                    estoque=estoque, 
                    nome_categoria=cat_nome,
                    imagem_path=self.imagem_path # Passamos a nova imagem
                )
                messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
            
            # 4. Redireciona de volta para a listagem
            self.controller.show_view("ManageProducts", data=self.usuario)
            
        except ValueError as ve:
            # Erros de validação (ex: preço inválido) mostram aviso amarelo
            messagebox.showwarning("Atenção", str(ve))
        except Exception as e:
            # Erros inesperados (ex: banco fora do ar) mostram erro vermelho
            print("ERRO AO SALVAR:")
            traceback.print_exc()
            messagebox.showerror("Erro Crítico", f"Não foi possível salvar: {e}")