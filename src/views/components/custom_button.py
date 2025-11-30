import tkinter as tk
from src.config.settings import Config

class CustomButton(tk.Button):
    """
    Botão customizado com estilos predefinidos do sistema.
    
    Variantes:
    - primary: Azul (ações principais)
    - secondary: Vermelho (ações de cancelamento/exclusão)
    - accent: Verde (ações de sucesso/confirmação)
    - outline: Borda colorida com fundo transparente
    """
    
    def __init__(self, parent, text, command=None, variant="primary", width=None, **kwargs):
        """
        Args:
            parent: Widget pai
            text: Texto do botão
            command: Função callback
            variant: Tipo de botão (primary, secondary, accent, outline)
            width: Largura do botão (None = automático)
            **kwargs: Argumentos adicionais do tk.Button
        """
        # Define as cores baseadas na variante
        styles = self._get_variant_style(variant)
        
        # Configuração padrão
        config = {
            'text': text,
            'command': command,
            'font': Config.FONT_BODY,
            'cursor': 'hand2',
            'relief': 'flat',
            'padx': 20,
            'pady': 10,
            **styles,
            **kwargs  # Permite sobrescrever qualquer configuração
        }
        
        if width:
            config['width'] = width
            
        super().__init__(parent, **config)
        
        # Efeitos de hover
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
        
        # Armazena cores originais
        self.original_bg = styles['bg']
        self.original_fg = styles['fg']
        self.variant = variant
    
    def _get_variant_style(self, variant):
        """Retorna o estilo baseado na variante."""
        styles = {
            'primary': {
                'bg': Config.COLOR_PRIMARY,
                'fg': 'white',
                'activebackground': '#2563EB',  # Azul mais escuro
                'activeforeground': 'white'
            },
            'secondary': {
                'bg': Config.COLOR_SECONDARY,
                'fg': 'white',
                'activebackground': '#DC2626',  # Vermelho mais escuro
                'activeforeground': 'white'
            },
            'accent': {
                'bg': Config.COLOR_ACCENT,
                'fg': 'white',
                'activebackground': '#16A34A',  # Verde mais escuro
                'activeforeground': 'white'
            },
            'outline': {
                'bg': Config.COLOR_WHITE,
                'fg': Config.COLOR_PRIMARY,
                'activebackground': Config.COLOR_BG,
                'activeforeground': Config.COLOR_PRIMARY,
                'highlightbackground': Config.COLOR_PRIMARY,
                'highlightthickness': 2
            },
            'light': {
                'bg': Config.COLOR_BG,
                'fg': Config.COLOR_TEXT,
                'activebackground': '#D1D5DB',
                'activeforeground': Config.COLOR_TEXT
            }
        }
        
        return styles.get(variant, styles['primary'])
    
    def _on_enter(self, event):
        """Efeito ao passar o mouse."""
        if self['state'] != 'disabled':
            if self.variant == 'primary':
                self['bg'] = '#2563EB'
            elif self.variant == 'secondary':
                self['bg'] = '#DC2626'
            elif self.variant == 'accent':
                self['bg'] = '#16A34A'
            elif self.variant == 'outline':
                self['bg'] = Config.COLOR_BG
            elif self.variant == 'light':
                self['bg'] = '#D1D5DB'
    
    def _on_leave(self, event):
        """Restaura cor original ao sair."""
        if self['state'] != 'disabled':
            self['bg'] = self.original_bg


class IconButton(tk.Button):
    """
    Botão compacto com ícone/símbolo (usando caracteres Unicode).
    Útil para ações secundárias como editar, excluir, etc.
    """
    
    ICONS = {
        'edit': '✏️',
        'delete': '🗑️',
        'add': '➕',
        'remove': '➖',
        'check': '✓',
        'close': '✕',
        'search': '🔍',
        'refresh': '🔄',
        'save': '💾',
        'download': '⬇️',
        'upload': '⬆️',
        'settings': '⚙️',
        'info': 'ℹ️',
        'warning': '⚠️',
        'cart': '🛒',
        'user': '👤'
    }
    
    def __init__(self, parent, icon='check', command=None, tooltip=None, **kwargs):
        """
        Args:
            parent: Widget pai
            icon: Nome do ícone ou caractere direto
            command: Função callback
            tooltip: Texto de ajuda ao passar o mouse
            **kwargs: Argumentos adicionais
        """
        # Busca o ícone ou usa o texto direto
        icon_text = self.ICONS.get(icon, icon)
        
        config = {
            'text': icon_text,
            'command': command,
            'font': ('Arial', 14),
            'bg': Config.COLOR_BG,
            'fg': Config.COLOR_TEXT,
            'relief': 'flat',
            'cursor': 'hand2',
            'padx': 8,
            'pady': 8,
            'width': 3,
            **kwargs
        }
        
        super().__init__(parent, **config)
        
        # Efeito hover
        self.bind('<Enter>', lambda e: self.config(bg=Config.COLOR_PRIMARY, fg='white'))
        self.bind('<Leave>', lambda e: self.config(bg=Config.COLOR_BG, fg=Config.COLOR_TEXT))
        
        # Tooltip simples
        if tooltip:
            self._create_tooltip(tooltip)
    
    def _create_tooltip(self, text):
        """Cria tooltip ao passar o mouse."""
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = tk.Label(
                tooltip, 
                text=text, 
                bg='#1F2937', 
                fg='white',
                font=Config.FONT_SMALL,
                padx=8,
                pady=4
            )
            label.pack()
            
            self.tooltip_window = tooltip
        
        def hide_tooltip(event):
            if hasattr(self, 'tooltip_window'):
                self.tooltip_window.destroy()
        
        self.bind('<Enter>', lambda e: [show_tooltip(e), self.config(bg=Config.COLOR_PRIMARY, fg='white')])
        self.bind('<Leave>', lambda e: [hide_tooltip(e), self.config(bg=Config.COLOR_BG, fg=Config.COLOR_TEXT)])
