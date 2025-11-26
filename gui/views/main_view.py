"""
Tela Principal - SCEE
Dashboard com navegação para todas as funcionalidades
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging

logger = logging.getLogger(__name__)


class MainView:
    """Tela principal da aplicação"""
    
    def __init__(self, parent, user_data, on_logout_callback):
        """
        Inicializa a view principal
        
        Args:
            parent: Widget pai (janela principal)
            user_data: Dados do usuário logado
            on_logout_callback: Função chamada quando usuário faz logout
        """
        self.parent = parent
        self.user_data = user_data
        self.on_logout_callback = on_logout_callback
        
        # Criar interface
        self.create_widgets()
        
    def create_widgets(self):
        """Cria os widgets da tela principal"""
        
        # Container principal
        self.main_frame = tk.Frame(self.parent, bg='#f8fafc')
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Barra superior (header)
        self.create_header()
        
        # Barra lateral (sidebar)
        self.create_sidebar()
        
        # Área de conteúdo
        self.create_content_area()
        
    def create_header(self):
        """Cria a barra superior"""
        header_frame = tk.Frame(self.main_frame, bg='#2563eb', height=60)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)
        
        # Logo e título
        title_label = tk.Label(
            header_frame,
            text="🛒 SCEE - Sistema de Comércio Eletrônico",
            font=('Arial', 16, 'bold'),
            bg='#2563eb',
            fg='#ffffff'
        )
        title_label.pack(side=tk.LEFT, padx=20)
        
        # Informações do usuário
        user_frame = tk.Frame(header_frame, bg='#2563eb')
        user_frame.pack(side=tk.RIGHT, padx=20)
        
        user_label = tk.Label(
            user_frame,
            text=f"👤 {self.user_data.get('nome', 'Usuário')}",
            font=('Arial', 11),
            bg='#2563eb',
            fg='#ffffff'
        )
        user_label.pack(side=tk.LEFT, padx=10)
        
        logout_button = tk.Button(
            user_frame,
            text="Sair",
            font=('Arial', 10),
            bg='#dc2626',
            fg='#ffffff',
            activebackground='#b91c1c',
            activeforeground='#ffffff',
            relief=tk.FLAT,
            cursor='hand2',
            command=self.logout,
            padx=15,
            pady=5
        )
        logout_button.pack(side=tk.LEFT)
        
    def create_sidebar(self):
        """Cria a barra lateral com menu de navegação"""
        sidebar_frame = tk.Frame(self.main_frame, bg='#1e293b', width=250)
        sidebar_frame.pack(fill=tk.Y, side=tk.LEFT)
        sidebar_frame.pack_propagate(False)
        
        # Título do menu
        menu_title = tk.Label(
            sidebar_frame,
            text="Menu Principal",
            font=('Arial', 14, 'bold'),
            bg='#1e293b',
            fg='#ffffff',
            pady=20
        )
        menu_title.pack(fill=tk.X)
        
        # Separador
        separator = tk.Frame(sidebar_frame, bg='#334155', height=2)
        separator.pack(fill=tk.X, padx=20, pady=10)
        
        # Botões do menu
        menu_items = [
            ("🏠 Dashboard", self.show_dashboard),
            ("📦 Produtos", self.show_produtos),
            ("🏷️ Categorias", self.show_categorias),
            ("🛒 Carrinho", self.show_carrinho),
            ("📋 Pedidos", self.show_pedidos),
        ]
        
        # Adicionar opções de admin se for administrador
        if self.user_data.get('tipo_usuario') == 'ADMINISTRADOR':
            menu_items.extend([
                ("", None),  # Separador
                ("👥 Clientes", self.show_clientes),
                ("⚙️ Administração", self.show_admin),
            ])
        
        for item_text, command in menu_items:
            if not item_text:  # Separador
                separator = tk.Frame(sidebar_frame, bg='#334155', height=1)
                separator.pack(fill=tk.X, padx=20, pady=10)
                continue
                
            button = tk.Button(
                sidebar_frame,
                text=item_text,
                font=('Arial', 11),
                bg='#1e293b',
                fg='#ffffff',
                activebackground='#334155',
                activeforeground='#ffffff',
                relief=tk.FLAT,
                cursor='hand2',
                command=command,
                anchor=tk.W,
                padx=20,
                pady=12
            )
            button.pack(fill=tk.X, padx=10, pady=2)
            
            # Hover effect
            button.bind('<Enter>', lambda e, b=button: b.configure(bg='#334155'))
            button.bind('<Leave>', lambda e, b=button: b.configure(bg='#1e293b'))
        
    def create_content_area(self):
        """Cria a área de conteúdo"""
        self.content_frame = tk.Frame(self.main_frame, bg='#f8fafc')
        self.content_frame.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)
        
        # Mostrar dashboard por padrão
        self.show_dashboard()
        
    def clear_content(self):
        """Limpa a área de conteúdo"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
    def show_dashboard(self):
        """Mostra o dashboard"""
        self.clear_content()
        
        # Título
        title = tk.Label(
            self.content_frame,
            text="📊 Dashboard",
            font=('Arial', 24, 'bold'),
            bg='#f8fafc',
            fg='#1e293b'
        )
        title.pack(pady=30, padx=30, anchor=tk.W)
        
        # Cards de estatísticas
        cards_frame = tk.Frame(self.content_frame, bg='#f8fafc')
        cards_frame.pack(fill=tk.BOTH, expand=True, padx=30)
        
        # Exemplo de cards (será implementado com dados reais)
        cards = [
            ("📦 Produtos", "150 itens", "#3b82f6"),
            ("🛒 Carrinho", "5 itens", "#10b981"),
            ("📋 Pedidos", "23 pedidos", "#f59e0b"),
            ("👥 Clientes", "89 clientes", "#8b5cf6"),
        ]
        
        for i, (title, value, color) in enumerate(cards):
            card = tk.Frame(cards_frame, bg='#ffffff', relief=tk.RAISED, borderwidth=1)
            card.grid(row=i//2, column=i%2, padx=15, pady=15, sticky='nsew', ipadx=30, ipady=30)
            
            tk.Label(
                card,
                text=title,
                font=('Arial', 14),
                bg='#ffffff',
                fg='#64748b'
            ).pack(pady=(10, 5))
            
            tk.Label(
                card,
                text=value,
                font=('Arial', 28, 'bold'),
                bg='#ffffff',
                fg=color
            ).pack()
            
        # Configurar grid
        cards_frame.grid_columnconfigure(0, weight=1)
        cards_frame.grid_columnconfigure(1, weight=1)
        
    def show_produtos(self):
        """Mostra a tela de produtos"""
        self.clear_content()
        label = tk.Label(
            self.content_frame,
            text="📦 Produtos - Em desenvolvimento",
            font=('Arial', 24),
            bg='#f8fafc'
        )
        label.pack(pady=100)
        
    def show_categorias(self):
        """Mostra a tela de categorias"""
        self.clear_content()
        label = tk.Label(
            self.content_frame,
            text="🏷️ Categorias - Em desenvolvimento",
            font=('Arial', 24),
            bg='#f8fafc'
        )
        label.pack(pady=100)
        
    def show_carrinho(self):
        """Mostra a tela de carrinho"""
        self.clear_content()
        label = tk.Label(
            self.content_frame,
            text="🛒 Carrinho - Em desenvolvimento",
            font=('Arial', 24),
            bg='#f8fafc'
        )
        label.pack(pady=100)
        
    def show_pedidos(self):
        """Mostra a tela de pedidos"""
        self.clear_content()
        label = tk.Label(
            self.content_frame,
            text="📋 Pedidos - Em desenvolvimento",
            font=('Arial', 24),
            bg='#f8fafc'
        )
        label.pack(pady=100)
        
    def show_clientes(self):
        """Mostra a tela de clientes (admin)"""
        self.clear_content()
        label = tk.Label(
            self.content_frame,
            text="👥 Clientes - Em desenvolvimento",
            font=('Arial', 24),
            bg='#f8fafc'
        )
        label.pack(pady=100)
        
    def show_admin(self):
        """Mostra a tela de administração"""
        self.clear_content()
        label = tk.Label(
            self.content_frame,
            text="⚙️ Administração - Em desenvolvimento",
            font=('Arial', 24),
            bg='#f8fafc'
        )
        label.pack(pady=100)
        
    def logout(self):
        """Realiza o logout"""
        result = messagebox.askyesno(
            "Confirmar Logout",
            "Tem certeza que deseja sair?"
        )
        
        if result and self.on_logout_callback:
            self.on_logout_callback()
