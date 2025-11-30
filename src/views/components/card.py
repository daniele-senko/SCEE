import tkinter as tk
from abc import ABC, abstractmethod
from typing import Optional, Callable
from src.config.settings import Config


class BaseCard(tk.Frame, ABC):
    """
    Classe abstrata base para todos os cards.
    Implementa Template Method Pattern para estrutura comum.
    """
    
    def __init__(self, parent, padding=20, elevation=True, bg=Config.COLOR_WHITE, **kwargs):
        """
        Args:
            parent: Widget pai
            padding: Espaçamento interno
            elevation: Adiciona sombra/borda
            bg: Cor de fundo
            **kwargs: Argumentos adicionais do tk.Frame
        """
        # Configuração de elevation (Decorator Pattern)
        self._setup_elevation(parent, elevation)
        
        # Inicializa Frame
        if elevation:
            super().__init__(self._shadow_frame, bg=bg, padx=padding, pady=padding, **kwargs)
        else:
            super().__init__(parent, bg=bg, padx=padding, pady=padding, **kwargs)
        
        self.pack(fill="both", expand=True)
        self.bg_color = bg
        
        # Template Method: define estrutura, subclasses implementam detalhes
        self._build_card()
    
    def _setup_elevation(self, parent, elevation):
        """Configura efeito de elevação (sombra)."""
        if elevation:
            self._shadow_frame = tk.Frame(parent, bg='#D1D5DB')
            self._shadow_frame.pack(fill="both", expand=True, padx=2, pady=2)
    
    @abstractmethod
    def _build_card(self):
        """
        Template Method: cada tipo de card implementa sua estrutura.
        Este método deve ser sobrescrito pelas subclasses.
        """
        pass
    
    def clear_content(self):
        """Remove todo o conteúdo do card."""
        for widget in self.winfo_children():
            widget.destroy()


class Card(BaseCard):
    """
    Card genérico com título, subtítulo e área de conteúdo.
    Usa Composition Pattern para gerenciar componentes internos.
    """
    
    def __init__(self, parent, title: Optional[str] = None, 
                 subtitle: Optional[str] = None, **kwargs):
        """
        Args:
            parent: Widget pai
            title: Título do card
            subtitle: Subtítulo/descrição
            **kwargs: Argumentos para BaseCard
        """
        self._title = title
        self._subtitle = subtitle
        self._header = None
        self.content = None
        
        super().__init__(parent, **kwargs)
    
    def _build_card(self):
        """Implementa estrutura do card genérico."""
        # Cabeçalho (se houver título)
        if self._title:
            self._header = self._create_header()
        
        # Container de conteúdo
        self.content = tk.Frame(self, bg=self.bg_color)
        self.content.pack(fill="both", expand=True, pady=(10 if self._title else 0, 0))
    
    def _create_header(self) -> tk.Frame:
        """Cria e retorna o cabeçalho do card."""
        header = tk.Frame(self, bg=self.bg_color)
        header.pack(fill="x", pady=(0, 10))
        
        # Título
        tk.Label(
            header,
            text=self._title,
            font=Config.FONT_HEADER,
            bg=self.bg_color,
            fg=Config.COLOR_TEXT
        ).pack(anchor="w")
        
        # Subtítulo
        if self._subtitle:
            tk.Label(
                header,
                text=self._subtitle,
                font=Config.FONT_SMALL,
                bg=self.bg_color,
                fg=Config.COLOR_TEXT_LIGHT
            ).pack(anchor="w")
        
        return header
    
    def add_widget(self, widget) -> tk.Widget:
        """
        Adiciona um widget ao conteúdo do card.
        
        Args:
            widget: Widget a ser adicionado
            
        Returns:
            O widget adicionado (para encadeamento)
        """
        widget.pack(in_=self.content, fill="x", pady=5)
        return widget
    
    def set_title(self, title: str):
        """Atualiza o título dinamicamente."""
        self._title = title
        if self._header:
            self._header.destroy()
            self._header = self._create_header()
    
    def clear_content(self):
        """Remove apenas o conteúdo, mantendo o cabeçalho."""
        if self.content:
            for widget in self.content.winfo_children():
                widget.destroy()


class StatCard(BaseCard):
    """
    Card de estatística (número grande com label).
    Herda de BaseCard e especializa para exibição de métricas.
    """
    
    def __init__(self, parent, label: str, value: str, 
                 icon: Optional[str] = None, color: str = Config.COLOR_PRIMARY, **kwargs):
        """
        Args:
            parent: Widget pai
            label: Texto descritivo
            value: Valor a exibir
            icon: Emoji/caractere do ícone
            color: Cor do ícone/valor
            **kwargs: Argumentos para BaseCard
        """
        self._label = label
        self._value = value
        self._icon = icon
        self._color = color
        
        # Widgets que serão criados
        self._icon_label = None
        self._value_label = None
        self._desc_label = None
        
        # Define estilo padrão para StatCard
        kwargs.setdefault('elevation', True)
        kwargs.setdefault('padding', 20)
        
        super().__init__(parent, **kwargs)
    
    def _build_card(self):
        """Implementa estrutura do card de estatística."""
        # Ícone (se fornecido)
        if self._icon:
            self._icon_label = tk.Label(
                self,
                text=self._icon,
                font=('TkDefaultFont', 24),
                bg=self.bg_color,
                fg=self._color
            )
            self._icon_label.pack(anchor="w")
        
        # Valor (grande e destacado)
        self._value_label = tk.Label(
            self,
            text=str(self._value),
            font=('TkDefaultFont', 28, 'bold'),
            bg=self.bg_color,
            fg=self._color
        )
        self._value_label.pack(anchor="w")
        
        # Label descritivo
        self._desc_label = tk.Label(
            self,
            text=self._label,
            font=Config.FONT_SMALL,
            bg=self.bg_color,
            fg=Config.COLOR_TEXT_LIGHT
        )
        self._desc_label.pack(anchor="w")
    
    def update_value(self, new_value: str):
        """
        Atualiza o valor exibido dinamicamente.
        
        Args:
            new_value: Novo valor a ser exibido
        """
        self._value = new_value
        if self._value_label:
            self._value_label.config(text=str(new_value))
    
    def update_label(self, new_label: str):
        """Atualiza o label descritivo."""
        self._label = new_label
        if self._desc_label:
            self._desc_label.config(text=new_label)
    
    def set_color(self, color: str):
        """Altera a cor do ícone e valor."""
        self._color = color
        if self._icon_label:
            self._icon_label.config(fg=color)
        if self._value_label:
            self._value_label.config(fg=color)


class InfoCard(BaseCard):
    """
    Card de informação com ícone, título e descrição.
    Implementa Observer Pattern para permitir callbacks de clique.
    """
    
    def __init__(self, parent, title: str, description: str, 
                 icon: Optional[str] = None, icon_bg: str = Config.COLOR_PRIMARY, 
                 clickable: bool = False, on_click: Optional[Callable] = None, **kwargs):
        """
        Args:
            parent: Widget pai
            title: Título
            description: Descrição
            icon: Emoji/caractere
            icon_bg: Cor de fundo do ícone
            clickable: Se o card é clicável
            on_click: Callback ao clicar
            **kwargs: Argumentos para BaseCard
        """
        self._title = title
        self._description = description
        self._icon = icon
        self._icon_bg = icon_bg
        self._clickable = clickable
        self._on_click = on_click
        
        # Widgets internos
        self._title_label = None
        self._desc_label = None
        
        kwargs.setdefault('padding', 15)
        kwargs.setdefault('elevation', True)
        
        super().__init__(parent, **kwargs)
        
        # Configura interatividade
        if clickable:
            self._make_clickable()
    
    def _build_card(self):
        """Implementa estrutura do card de informação."""
        # Layout horizontal
        if self._icon:
            self._create_icon()
        
        # Texto à direita
        self._create_text_section()
    
    def _create_icon(self):
        """Cria seção do ícone."""
        icon_frame = tk.Frame(self, bg=self._icon_bg, width=50, height=50)
        icon_frame.pack(side="left", padx=(0, 15))
        icon_frame.pack_propagate(False)
        
        tk.Label(
            icon_frame,
            text=self._icon,
            font=('TkDefaultFont', 24),
            bg=self._icon_bg,
            fg='white'
        ).place(relx=0.5, rely=0.5, anchor='center')
    
    def _create_text_section(self):
        """Cria seção de texto."""
        text_frame = tk.Frame(self, bg=self.bg_color)
        text_frame.pack(side="left", fill="both", expand=True)
        
        self._title_label = tk.Label(
            text_frame,
            text=self._title,
            font=Config.FONT_BODY,
            bg=self.bg_color,
            fg=Config.COLOR_TEXT,
            anchor='w'
        )
        self._title_label.pack(fill="x")
        
        self._desc_label = tk.Label(
            text_frame,
            text=self._description,
            font=Config.FONT_SMALL,
            bg=self.bg_color,
            fg=Config.COLOR_TEXT_LIGHT,
            anchor='w',
            wraplength=300
        )
        self._desc_label.pack(fill="x")
    
    def _make_clickable(self):
        """Torna o card clicável."""
        self.config(cursor='hand2')
        
        # Bind em todos os widgets internos também
        def handle_click(event):
            if self._on_click:
                self._on_click()
        
        self.bind('<Button-1>', handle_click)
        for child in self.winfo_children():
            child.bind('<Button-1>', handle_click)
    
    def update_title(self, new_title: str):
        """Atualiza o título."""
        self._title = new_title
        if self._title_label:
            self._title_label.config(text=new_title)
    
    def update_description(self, new_description: str):
        """Atualiza a descrição."""
        self._description = new_description
        if self._desc_label:
            self._desc_label.config(text=new_description)
    
    def set_click_handler(self, callback: Callable):
        """Define ou altera o handler de clique."""
        self._on_click = callback
        if not self._clickable:
            self._clickable = True
            self._make_clickable()


class CollapsibleCard(BaseCard):
    """
    Card expansível/colapsável.
    Implementa State Pattern para gerenciar estados expandido/colapsado.
    """
    
    # Constantes para ícones
    ICON_COLLAPSED = "▶"
    ICON_EXPANDED = "▼"
    
    def __init__(self, parent, title: str, content_widgets: Optional[list] = None, 
                 start_expanded: bool = False, **kwargs):
        """
        Args:
            parent: Widget pai
            title: Título do card
            content_widgets: Lista de widgets para adicionar ao conteúdo
            start_expanded: Se deve iniciar expandido
            **kwargs: Argumentos para BaseCard
        """
        self._title = title
        self._content_widgets = content_widgets or []
        self._is_expanded = start_expanded
        
        # Componentes internos
        self._header = None
        self._expand_icon = None
        self.content = None
        
        kwargs.setdefault('padding', 0)
        kwargs.setdefault('elevation', True)
        
        super().__init__(parent, **kwargs)
        
        # Define estado inicial
        if start_expanded:
            self.expand()
        else:
            self.collapse()
    
    def _build_card(self):
        """Implementa estrutura do card colapsável."""
        # Cabeçalho clicável
        self._header = self._create_header()
        
        # Container de conteúdo
        self.content = tk.Frame(self, bg=self.bg_color, padx=20, pady=10)
        
        # Adiciona widgets iniciais
        for widget in self._content_widgets:
            widget.pack(in_=self.content, fill="x", pady=5)
    
    def _create_header(self) -> tk.Frame:
        """Cria cabeçalho clicável."""
        header = tk.Frame(self, bg=Config.COLOR_BG, cursor='hand2')
        header.pack(fill="x")
        header.bind('<Button-1>', self.toggle)
        
        # Ícone de expansão
        self._expand_icon = tk.Label(
            header,
            text=self.ICON_EXPANDED if self._is_expanded else self.ICON_COLLAPSED,
            font=Config.FONT_BODY,
            bg=Config.COLOR_BG,
            fg=Config.COLOR_TEXT
        )
        self._expand_icon.pack(side="left", padx=10, pady=10)
        self._expand_icon.bind('<Button-1>', self.toggle)
        
        # Título
        title_label = tk.Label(
            header,
            text=self._title,
            font=Config.FONT_BODY,
            bg=Config.COLOR_BG,
            fg=Config.COLOR_TEXT
        )
        title_label.pack(side="left", fill="x", expand=True, pady=10)
        title_label.bind('<Button-1>', self.toggle)
        
        return header
    
    def toggle(self, event=None):
        """
        Alterna entre expandido/colapsado.
        
        Args:
            event: Evento do Tkinter (opcional)
        """
        if self._is_expanded:
            self.collapse()
        else:
            self.expand()
    
    def expand(self):
        """Expande o card mostrando o conteúdo."""
        if not self._is_expanded:
            self.content.pack(fill="x", padx=0, pady=(0, 10))
            if self._expand_icon:
                self._expand_icon.config(text=self.ICON_EXPANDED)
            self._is_expanded = True
    
    def collapse(self):
        """Colapsa o card ocultando o conteúdo."""
        if self._is_expanded:
            self.content.pack_forget()
            if self._expand_icon:
                self._expand_icon.config(text=self.ICON_COLLAPSED)
            self._is_expanded = False
    
    def add_content(self, widget) -> tk.Widget:
        """
        Adiciona widget ao conteúdo.
        
        Args:
            widget: Widget a ser adicionado
            
        Returns:
            O widget adicionado
        """
        widget.pack(in_=self.content, fill="x", pady=5)
        return widget
    
    @property
    def is_expanded(self) -> bool:
        """Retorna se o card está expandido."""
        return self._is_expanded
    
    def set_title(self, new_title: str):
        """Atualiza o título do card."""
        self._title = new_title
        # Reconstrói header
        if self._header:
            self._header.destroy()
            self._header = self._create_header()
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
