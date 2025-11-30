import tkinter as tk
from src.config.settings import Config

class Modal(tk.Toplevel):
    """
    Modal genérico customizável para mensagens e confirmações.
    """
    
    def __init__(self, parent, title="", message="", modal_type="info", buttons=None, on_confirm=None):
        """
        Args:
            parent: Janela pai
            title: Título do modal
            message: Mensagem principal
            modal_type: Tipo (info, success, warning, error, confirm)
            buttons: Lista de botões customizados ou None para padrão
            on_confirm: Callback ao confirmar (para modais de confirmação)
        """
        super().__init__(parent)
        
        self.result = None
        self.on_confirm = on_confirm
        
        # Configuração da janela
        self.title(title or "Mensagem")
        self.resizable(False, False)
        self.configure(bg=Config.COLOR_WHITE)
        
        # Centraliza na tela pai
        self.transient(parent)
        self.grab_set()
        
        # Conteúdo
        self._setup_ui(title, message, modal_type, buttons)
        
        # Centraliza
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - self.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")
    
    def _setup_ui(self, title, message, modal_type, buttons):
        """Configura a interface do modal."""
        # Container principal
        container = tk.Frame(self, bg=Config.COLOR_WHITE, padx=30, pady=20)
        container.pack(fill="both", expand=True)
        
        # Ícone baseado no tipo
        icons = {
            'info': 'ℹ️',
            'success': '✓',
            'warning': '⚠️',
            'error': '✕',
            'confirm': '❓'
        }
        
        colors = {
            'info': Config.COLOR_PRIMARY,
            'success': Config.COLOR_ACCENT,
            'warning': '#F59E0B',
            'error': Config.COLOR_SECONDARY,
            'confirm': Config.COLOR_PRIMARY
        }
        
        icon = icons.get(modal_type, 'ℹ️')
        color = colors.get(modal_type, Config.COLOR_PRIMARY)
        
        # Cabeçalho com ícone
        header = tk.Frame(container, bg=Config.COLOR_WHITE)
        header.pack(fill="x", pady=(0, 15))
        
        tk.Label(
            header,
            text=icon,
            font=('TkDefaultFont', 32),
            bg=Config.COLOR_WHITE,
            fg=color
        ).pack()
        
        if title:
            tk.Label(
                header,
                text=title,
                font=Config.FONT_HEADER,
                bg=Config.COLOR_WHITE,
                fg=color
            ).pack(pady=(10, 0))
        
        # Mensagem
        tk.Label(
            container,
            text=message,
            font=Config.FONT_BODY,
            bg=Config.COLOR_WHITE,
            fg=Config.COLOR_TEXT,
            wraplength=350,
            justify="center"
        ).pack(pady=(0, 20))
        
        # Botões
        btn_frame = tk.Frame(container, bg=Config.COLOR_WHITE)
        btn_frame.pack()
        
        if buttons:
            # Botões customizados
            for btn_config in buttons:
                tk.Button(
                    btn_frame,
                    text=btn_config.get('text', 'OK'),
                    command=lambda cmd=btn_config.get('command'): self._on_button_click(cmd),
                    bg=btn_config.get('bg', Config.COLOR_PRIMARY),
                    fg=btn_config.get('fg', 'white'),
                    font=Config.FONT_BODY,
                    padx=20,
                    pady=8,
                    cursor='hand2',
                    relief='flat'
                ).pack(side="left", padx=5)
        else:
            # Botões padrão baseados no tipo
            if modal_type == 'confirm':
                # Cancelar + Confirmar
                tk.Button(
                    btn_frame,
                    text="Cancelar",
                    command=lambda: self._on_button_click(False),
                    bg=Config.COLOR_TEXT_LIGHT,
                    fg='white',
                    font=Config.FONT_BODY,
                    padx=20,
                    pady=8,
                    cursor='hand2',
                    relief='flat'
                ).pack(side="left", padx=5)
                
                tk.Button(
                    btn_frame,
                    text="Confirmar",
                    command=lambda: self._on_button_click(True),
                    bg=Config.COLOR_PRIMARY,
                    fg='white',
                    font=Config.FONT_BODY,
                    padx=20,
                    pady=8,
                    cursor='hand2',
                    relief='flat'
                ).pack(side="left", padx=5)
            else:
                # Apenas OK
                tk.Button(
                    btn_frame,
                    text="OK",
                    command=lambda: self._on_button_click(True),
                    bg=color,
                    fg='white',
                    font=Config.FONT_BODY,
                    padx=30,
                    pady=8,
                    cursor='hand2',
                    relief='flat'
                ).pack()
    
    def _on_button_click(self, result):
        """Callback ao clicar em um botão."""
        self.result = result
        if result and self.on_confirm:
            self.on_confirm()
        self.destroy()
    
    def show(self):
        """Mostra o modal e espera resposta."""
        self.wait_window()
        return self.result


class LoadingModal(tk.Toplevel):
    """
    Modal de carregamento com animação.
    """
    
    def __init__(self, parent, message="Carregando..."):
        super().__init__(parent)
        
        # Configuração
        self.overrideredirect(True)  # Remove bordas
        self.configure(bg=Config.COLOR_WHITE)
        
        # Container
        container = tk.Frame(self, bg=Config.COLOR_WHITE, padx=40, pady=30, relief='solid', bd=1)
        container.pack()
        
        # Animação de loading (usando caracteres)
        self.loading_label = tk.Label(
            container,
            text="⏳",
            font=('TkDefaultFont', 32),
            bg=Config.COLOR_WHITE,
            fg=Config.COLOR_PRIMARY
        )
        self.loading_label.pack()
        
        # Mensagem
        tk.Label(
            container,
            text=message,
            font=Config.FONT_BODY,
            bg=Config.COLOR_WHITE,
            fg=Config.COLOR_TEXT
        ).pack(pady=(10, 0))
        
        # Centraliza
        self.transient(parent)
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - self.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")
        
        # Inicia animação
        self.animation_chars = ['⏳', '⌛', '⏳', '⌛']
        self.animation_index = 0
        self._animate()
    
    def _animate(self):
        """Anima o ícone de loading."""
        if self.winfo_exists():
            self.loading_label.config(text=self.animation_chars[self.animation_index])
            self.animation_index = (self.animation_index + 1) % len(self.animation_chars)
            self.after(500, self._animate)
    
    def close(self):
        """Fecha o modal."""
        self.destroy()


class ToastNotification:
    """
    Notificação toast (mensagem temporária no canto da tela).
    """
    
    @staticmethod
    def show(parent, message, duration=3000, position='bottom', toast_type='info'):
        """
        Mostra notificação toast.
        
        Args:
            parent: Janela pai
            message: Mensagem
            duration: Duração em ms (0 = indefinido)
            position: Posição (top, bottom)
            toast_type: Tipo (info, success, warning, error)
        """
        # Cores baseadas no tipo
        colors = {
            'info': Config.COLOR_PRIMARY,
            'success': Config.COLOR_ACCENT,
            'warning': '#F59E0B',
            'error': Config.COLOR_SECONDARY
        }
        
        bg_color = colors.get(toast_type, Config.COLOR_PRIMARY)
        
        # Cria janela toast
        toast = tk.Toplevel(parent)
        toast.overrideredirect(True)
        toast.configure(bg=bg_color)
        
        # Container
        container = tk.Frame(toast, bg=bg_color, padx=20, pady=12)
        container.pack()
        
        # Mensagem
        tk.Label(
            container,
            text=message,
            font=Config.FONT_BODY,
            bg=bg_color,
            fg='white'
        ).pack()
        
        # Posiciona
        toast.update_idletasks()
        parent.update_idletasks()
        
        x = parent.winfo_x() + (parent.winfo_width() - toast.winfo_width()) // 2
        
        if position == 'top':
            y = parent.winfo_y() + 20
        else:  # bottom
            y = parent.winfo_y() + parent.winfo_height() - toast.winfo_height() - 20
        
        toast.geometry(f"+{x}+{y}")
        
        # Auto-fecha
        if duration > 0:
            toast.after(duration, toast.destroy)
        
        return toast


# Funções de conveniência
def show_info(parent, title, message):
    """Mostra modal de informação."""
    return Modal(parent, title, message, modal_type='info').show()

def show_success(parent, title, message):
    """Mostra modal de sucesso."""
    return Modal(parent, title, message, modal_type='success').show()

def show_warning(parent, title, message):
    """Mostra modal de aviso."""
    return Modal(parent, title, message, modal_type='warning').show()

def show_error(parent, title, message):
    """Mostra modal de erro."""
    return Modal(parent, title, message, modal_type='error').show()

def show_confirm(parent, title, message, on_confirm=None):
    """Mostra modal de confirmação."""
    return Modal(parent, title, message, modal_type='confirm', on_confirm=on_confirm).show()
