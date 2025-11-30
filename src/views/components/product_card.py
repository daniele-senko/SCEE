import tkinter as tk
from PIL import Image, ImageTk
import os
from src.config.settings import Config

class ProductCard(tk.Frame):
    """
    Card visual de produto.
    Exibe imagem, nome, preço e botão de compra.
    """
    
    def __init__(self, parent, produto, on_add_cart=None):
        # Card com borda suave e sombra simulada (relief raised)
        super().__init__(parent, bg=Config.COLOR_WHITE, relief="raised", bd=1)
        self.produto = produto
        self.on_add_cart = on_add_cart
        
        # Tamanho fixo para uniformidade
        self.pack_propagate(False)
        self.configure(width=220, height=340)
        
        self._setup_ui()

    def _get_val(self, key, default=None):
        if isinstance(self.produto, dict):
            return self.produto.get(key, default)
        return getattr(self.produto, key, default)

    def _setup_ui(self):
        # 1. Área da Imagem (Superior)
        img_frame = tk.Frame(self, bg="white", height=180)
        img_frame.pack(fill="x", pady=10)
        img_frame.pack_propagate(False)
        
        image_path = self._get_image_path()
        self.photo = self._load_image(image_path)
        
        lbl_img = tk.Label(img_frame, image=self.photo, bg="white")
        lbl_img.place(relx=0.5, rely=0.5, anchor="center")
        
        # 2. Área de Conteúdo (Inferior)
        content_frame = tk.Frame(self, bg=Config.COLOR_WHITE, padx=15)
        content_frame.pack(fill="both", expand=True)
        
        # Categoria (Pequeno, cinza)
        cat = self._get_val('categoria')
        cat_nome = cat.nome if hasattr(cat, 'nome') else "Geral"
        tk.Label(
            content_frame, 
            text=cat_nome.upper(),
            font=("TkDefaultFont", 8),
            bg=Config.COLOR_WHITE,
            fg=Config.COLOR_TEXT_LIGHT
        ).pack(anchor="w")

        # Nome do Produto (Negrito)
        nome = self._get_val('nome', 'Sem Nome')
        if len(nome) > 22: nome = nome[:19] + "..."
        
        tk.Label(
            content_frame, 
            text=nome,
            font=("TkDefaultFont", 11, "bold"),
            bg=Config.COLOR_WHITE,
            fg=Config.COLOR_TEXT,
            wraplength=190,
            justify="left"
        ).pack(anchor="w", pady=(0, 5))
        
        # Preço (Destaque Azul)
        preco = self._get_val('preco', 0.0)
        tk.Label(
            content_frame, 
            text=f"R$ {preco:.2f}",
            font=("TkDefaultFont", 14, "bold"),
            bg=Config.COLOR_WHITE,
            fg=Config.COLOR_ACCENT
        ).pack(anchor="w")

        # Botão de Ação (Verde/Accent)
        btn_frame = tk.Frame(self, bg=Config.COLOR_WHITE, pady=15)
        btn_frame.pack(side="bottom", fill="x")
        
        tk.Button(
            btn_frame,
            text="ADICIONAR AO CARRINHO",
            bg=Config.COLOR_PRIMARY,
            fg="white",
            font=("TkDefaultFont", 9, "bold"),
            relief="flat",
            cursor="hand2",
            activebackground=Config.COLOR_ACCENT,
            activeforeground="white",
            command=lambda: self.on_add_cart(self.produto) if self.on_add_cart else None
        ).pack(fill="x", padx=15)

    def _get_image_path(self):
        img_principal = self._get_val('imagem_principal')
        if img_principal: return img_principal
        imagens = self._get_val('imagens', [])
        if imagens and len(imagens) > 0: return imagens[0]
        return None

    def _load_image(self, path):
        try:
            final_path = None
            if path:
                if os.path.isabs(path):
                    final_path = path
                else:
                    final_path = os.path.join(Config.BASE_DIR, path)
                
                if os.path.exists(final_path):
                    original = Image.open(final_path)
                    # Mantém proporção (contain)
                    original.thumbnail((160, 160))
                    return ImageTk.PhotoImage(original)
            
            # Placeholder elegante se falhar
            img = Image.new('RGB', (160, 160), color='#F3F4F6')
            return ImageTk.PhotoImage(img)
            
        except Exception as e:
            print(f"Erro img: {e}")
            img = Image.new('RGB', (160, 160), color='#FEE2E2') # Vermelho claro erro
            return ImageTk.PhotoImage(img)