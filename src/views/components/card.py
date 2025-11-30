import tkinter as tk
from src.config.settings import Config

class Card(tk.Frame):
    """
    Componente de card (container estilizado) reutilizável.
    """
    
    def __init__(self, parent, title=None, subtitle=None, padding=20, 
                 elevation=True, bg=Config.COLOR_WHITE):
        """
        Args:
            parent: Widget pai
            title: Título do card
            subtitle: Subtítulo/descrição
            padding: Espaçamento interno
            elevation: Adiciona sombra/borda
            bg: Cor de fundo
        """
        # Frame externo para simular sombra (elevation)
        if elevation:
            shadow = tk.Frame(parent, bg='#D1D5DB')
            shadow.pack(fill="both", expand=True, padx=2, pady=2)
            super().__init__(shadow, bg=bg, padx=padding, pady=padding)
        else:
            super().__init__(parent, bg=bg, padx=padding, pady=padding)
        
        self.pack(fill="both", expand=True)
        
        # Cabeçalho se houver título
        if title:
            self._create_header(title, subtitle)
        
        # Container de conteúdo
        self.content = tk.Frame(self, bg=bg)
        self.content.pack(fill="both", expand=True, pady=(10 if title else 0, 0))
    
    def _create_header(self, title, subtitle):
        """Cria cabeçalho do card."""
        header = tk.Frame(self, bg=self['bg'])
        header.pack(fill="x", pady=(0, 10))
        
        # Título
        tk.Label(
            header,
            text=title,
            font=Config.FONT_HEADER,
            bg=self['bg'],
            fg=Config.COLOR_TEXT
        ).pack(anchor="w")
        
        # Subtítulo
        if subtitle:
            tk.Label(
                header,
                text=subtitle,
                font=Config.FONT_SMALL,
                bg=self['bg'],
                fg=Config.COLOR_TEXT_LIGHT
            ).pack(anchor="w")
    
    def add_widget(self, widget):
        """Adiciona um widget ao conteúdo do card."""
        widget.pack(in_=self.content, fill="x", pady=5)
        return widget
    
    def clear_content(self):
        """Remove todo o conteúdo do card."""
        for widget in self.content.winfo_children():
            widget.destroy()


class StatCard(tk.Frame):
    """
    Card de estatística (número grande com label).
    """
    
    def __init__(self, parent, label, value, icon=None, color=Config.COLOR_PRIMARY):
        """
        Args:
            parent: Widget pai
            label: Texto descritivo
            value: Valor a exibir
            icon: Emoji/caractere do ícone
            color: Cor do ícone/valor
        """
        super().__init__(parent, bg=Config.COLOR_WHITE, relief='solid', bd=1)
        self.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Container interno
        container = tk.Frame(self, bg=Config.COLOR_WHITE, padx=20, pady=15)
        container.pack(fill="both", expand=True)
        
        # Ícone (se fornecido)
        if icon:
            tk.Label(
                container,
                text=icon,
                font=('Arial', 24),
                bg=Config.COLOR_WHITE,
                fg=color
            ).pack(anchor="w")
        
        # Valor
        tk.Label(
            container,
            text=str(value),
            font=('Arial', 28, 'bold'),
            bg=Config.COLOR_WHITE,
            fg=color
        ).pack(anchor="w")
        
        # Label
        tk.Label(
            container,
            text=label,
            font=Config.FONT_SMALL,
            bg=Config.COLOR_WHITE,
            fg=Config.COLOR_TEXT_LIGHT
        ).pack(anchor="w")


class InfoCard(tk.Frame):
    """
    Card de informação com ícone, título e descrição.
    """
    
    def __init__(self, parent, title, description, icon=None, 
                 icon_bg=Config.COLOR_PRIMARY, clickable=False, on_click=None):
        """
        Args:
            parent: Widget pai
            title: Título
            description: Descrição
            icon: Emoji/caractere
            icon_bg: Cor de fundo do ícone
            clickable: Se o card é clicável
            on_click: Callback ao clicar
        """
        super().__init__(parent, bg=Config.COLOR_WHITE, relief='solid', bd=1)
        self.pack(fill="x", padx=5, pady=5)
        
        if clickable:
            self.config(cursor='hand2')
            self.bind('<Button-1>', lambda e: on_click() if on_click else None)
        
        # Container
        container = tk.Frame(self, bg=Config.COLOR_WHITE, padx=15, pady=15)
        container.pack(fill="both", expand=True)
        
        # Layout horizontal
        if icon:
            # Ícone à esquerda
            icon_frame = tk.Frame(container, bg=icon_bg, width=50, height=50)
            icon_frame.pack(side="left", padx=(0, 15))
            icon_frame.pack_propagate(False)
            
            tk.Label(
                icon_frame,
                text=icon,
                font=('Arial', 24),
                bg=icon_bg,
                fg='white'
            ).place(relx=0.5, rely=0.5, anchor='center')
        
        # Texto à direita
        text_frame = tk.Frame(container, bg=Config.COLOR_WHITE)
        text_frame.pack(side="left", fill="both", expand=True)
        
        tk.Label(
            text_frame,
            text=title,
            font=Config.FONT_BODY,
            bg=Config.COLOR_WHITE,
            fg=Config.COLOR_TEXT,
            anchor='w'
        ).pack(fill="x")
        
        tk.Label(
            text_frame,
            text=description,
            font=Config.FONT_SMALL,
            bg=Config.COLOR_WHITE,
            fg=Config.COLOR_TEXT_LIGHT,
            anchor='w',
            wraplength=300
        ).pack(fill="x")


class CollapsibleCard(tk.Frame):
    """
    Card expansível/colapsável.
    """
    
    def __init__(self, parent, title, content_widgets=None):
        """
        Args:
            parent: Widget pai
            title: Título do card
            content_widgets: Lista de widgets para adicionar ao conteúdo
        """
        super().__init__(parent, bg=Config.COLOR_WHITE, relief='solid', bd=1)
        self.pack(fill="x", padx=5, pady=5)
        
        self.is_expanded = False
        
        # Cabeçalho (clicável)
        header = tk.Frame(self, bg=Config.COLOR_BG, cursor='hand2')
        header.pack(fill="x")
        header.bind('<Button-1>', self.toggle)
        
        # Ícone expansão
        self.expand_icon = tk.Label(
            header,
            text="▶",
            font=Config.FONT_BODY,
            bg=Config.COLOR_BG,
            fg=Config.COLOR_TEXT
        )
        self.expand_icon.pack(side="left", padx=10, pady=10)
        self.expand_icon.bind('<Button-1>', self.toggle)
        
        # Título
        title_label = tk.Label(
            header,
            text=title,
            font=Config.FONT_BODY,
            bg=Config.COLOR_BG,
            fg=Config.COLOR_TEXT
        )
        title_label.pack(side="left", fill="x", expand=True, pady=10)
        title_label.bind('<Button-1>', self.toggle)
        
        # Container de conteúdo (inicialmente oculto)
        self.content = tk.Frame(self, bg=Config.COLOR_WHITE, padx=20, pady=10)
        
        # Adiciona widgets se fornecidos
        if content_widgets:
            for widget in content_widgets:
                widget.pack(in_=self.content, fill="x", pady=5)
    
    def toggle(self, event=None):
        """Alterna entre expandido/colapsado."""
        if self.is_expanded:
            self.collapse()
        else:
            self.expand()
    
    def expand(self):
        """Expande o card."""
        self.content.pack(fill="x", padx=0, pady=(0, 10))
        self.expand_icon.config(text="▼")
        self.is_expanded = True
    
    def collapse(self):
        """Colapsa o card."""
        self.content.pack_forget()
        self.expand_icon.config(text="▶")
        self.is_expanded = False
    
    def add_content(self, widget):
        """Adiciona widget ao conteúdo."""
        widget.pack(in_=self.content, fill="x", pady=5)
