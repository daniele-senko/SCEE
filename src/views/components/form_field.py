import tkinter as tk
from tkinter import ttk
from src.config.settings import Config

class FormField(tk.Frame):
    """
    Campo de formulário reutilizável com label, entry e validação visual.
    """
    
    def __init__(self, parent, label, field_type="text", width=40, required=False, **kwargs):
        """
        Args:
            parent: Widget pai
            label: Texto do label
            field_type: Tipo do campo (text, password, number, email)
            width: Largura do campo
            required: Se o campo é obrigatório (mostra asterisco)
            **kwargs: Argumentos adicionais para o Entry
        """
        super().__init__(parent, bg=Config.COLOR_WHITE)
        
        self.field_type = field_type
        self.required = required
        self.error_label = None
        
        # Label
        label_text = f"{label} *" if required else label
        self.label = tk.Label(
            self, 
            text=label_text, 
            bg=Config.COLOR_WHITE, 
            font=Config.FONT_BODY,
            fg=Config.COLOR_TEXT
        )
        self.label.pack(anchor="w")
        
        # Entry
        entry_config = {
            'width': width,
            'font': Config.FONT_BODY,
            'bg': '#F8F9FA',
            'relief': 'solid',
            'bd': 1,
            **kwargs
        }
        
        if field_type == "password":
            entry_config['show'] = '*'
        
        self.entry = tk.Entry(self, **entry_config)
        self.entry.pack(pady=(0, 5), fill="x")
        
        # Validação em tempo real para números
        if field_type == "number":
            self.entry.config(validate='key', validatecommand=(self.register(self._validate_number), '%P'))
        
        # Placeholder para email
        if field_type == "email":
            self._set_placeholder("exemplo@email.com")
    
    def _validate_number(self, value):
        """Permite apenas números e ponto decimal."""
        if value == "":
            return True
        try:
            float(value)
            return True
        except ValueError:
            return False
    
    def _set_placeholder(self, placeholder):
        """Define um placeholder para o campo."""
        self.entry.insert(0, placeholder)
        self.entry.config(fg=Config.COLOR_TEXT_LIGHT)
        
        def on_focus_in(event):
            if self.entry.get() == placeholder:
                self.entry.delete(0, tk.END)
                self.entry.config(fg=Config.COLOR_TEXT)
        
        def on_focus_out(event):
            if not self.entry.get():
                self.entry.insert(0, placeholder)
                self.entry.config(fg=Config.COLOR_TEXT_LIGHT)
        
        self.entry.bind('<FocusIn>', on_focus_in)
        self.entry.bind('<FocusOut>', on_focus_out)
    
    def get(self):
        """Retorna o valor do campo."""
        return self.entry.get()
    
    def set(self, value):
        """Define o valor do campo."""
        self.entry.delete(0, tk.END)
        self.entry.insert(0, value)
    
    def clear(self):
        """Limpa o campo."""
        self.entry.delete(0, tk.END)
    
    def show_error(self, message):
        """Mostra mensagem de erro abaixo do campo."""
        if self.error_label:
            self.error_label.destroy()
        
        self.error_label = tk.Label(
            self,
            text=f"⚠ {message}",
            bg=Config.COLOR_WHITE,
            fg=Config.COLOR_SECONDARY,
            font=Config.FONT_SMALL
        )
        self.error_label.pack(anchor="w")
        self.entry.config(highlightbackground=Config.COLOR_SECONDARY, highlightthickness=2)
    
    def clear_error(self):
        """Remove a mensagem de erro."""
        if self.error_label:
            self.error_label.destroy()
            self.error_label = None
        self.entry.config(highlightthickness=0)
    
    def validate(self):
        """Valida o campo e retorna True/False."""
        self.clear_error()
        
        value = self.get().strip()
        
        # Validação de campo obrigatório
        if self.required and not value:
            self.show_error("Campo obrigatório")
            return False
        
        # Validação de email
        if self.field_type == "email" and value:
            if '@' not in value or '.' not in value:
                self.show_error("Email inválido")
                return False
        
        return True


class SearchField(tk.Frame):
    """
    Campo de busca com ícone e botão de limpar.
    """
    
    def __init__(self, parent, placeholder="Buscar...", on_search=None, width=40):
        """
        Args:
            parent: Widget pai
            placeholder: Texto placeholder
            on_search: Callback chamado ao digitar (recebe o texto)
            width: Largura do campo
        """
        super().__init__(parent, bg=Config.COLOR_WHITE)
        
        self.on_search = on_search
        
        # Container do campo
        field_container = tk.Frame(self, bg='#F8F9FA', relief='solid', bd=1)
        field_container.pack(fill="x", expand=True)
        
        # Ícone de busca
        tk.Label(
            field_container,
            text="🔍",
            bg='#F8F9FA',
            font=('Arial', 12)
        ).pack(side="left", padx=(10, 5))
        
        # Entry
        self.entry = tk.Entry(
            field_container,
            font=Config.FONT_BODY,
            bg='#F8F9FA',
            relief='flat',
            width=width
        )
        self.entry.pack(side="left", fill="x", expand=True, padx=5, pady=8)
        
        # Placeholder
        self.placeholder = placeholder
        self._set_placeholder()
        
        # Botão limpar (só aparece quando há texto)
        self.clear_btn = tk.Label(
            field_container,
            text="✕",
            bg='#F8F9FA',
            fg=Config.COLOR_TEXT_LIGHT,
            cursor='hand2',
            font=('Arial', 12)
        )
        self.clear_btn.pack(side="right", padx=10)
        self.clear_btn.pack_forget()  # Esconde inicialmente
        
        # Eventos
        self.entry.bind('<KeyRelease>', self._on_key_release)
        self.clear_btn.bind('<Button-1>', self._on_clear)
    
    def _set_placeholder(self):
        """Define placeholder."""
        self.entry.insert(0, self.placeholder)
        self.entry.config(fg=Config.COLOR_TEXT_LIGHT)
        
        def on_focus_in(event):
            if self.entry.get() == self.placeholder:
                self.entry.delete(0, tk.END)
                self.entry.config(fg=Config.COLOR_TEXT)
        
        def on_focus_out(event):
            if not self.entry.get():
                self.entry.insert(0, self.placeholder)
                self.entry.config(fg=Config.COLOR_TEXT_LIGHT)
                self.clear_btn.pack_forget()
        
        self.entry.bind('<FocusIn>', on_focus_in)
        self.entry.bind('<FocusOut>', on_focus_out)
    
    def _on_key_release(self, event):
        """Atualiza ao digitar."""
        text = self.get()
        
        # Mostra/esconde botão limpar
        if text and text != self.placeholder:
            self.clear_btn.pack(side="right", padx=10)
        else:
            self.clear_btn.pack_forget()
        
        # Chama callback
        if self.on_search and text != self.placeholder:
            self.on_search(text)
    
    def _on_clear(self, event):
        """Limpa o campo."""
        self.entry.delete(0, tk.END)
        self.clear_btn.pack_forget()
        if self.on_search:
            self.on_search("")
    
    def get(self):
        """Retorna o valor (sem placeholder)."""
        text = self.entry.get()
        return "" if text == self.placeholder else text
    
    def set(self, value):
        """Define o valor."""
        self.entry.delete(0, tk.END)
        if value:
            self.entry.insert(0, value)
            self.entry.config(fg=Config.COLOR_TEXT)
        else:
            self._set_placeholder()


class SelectField(tk.Frame):
    """
    Campo de seleção (combobox) customizado.
    """
    
    def __init__(self, parent, label, options=None, width=40, required=False):
        """
        Args:
            parent: Widget pai
            label: Texto do label
            options: Lista de opções
            width: Largura do campo
            required: Se é obrigatório
        """
        super().__init__(parent, bg=Config.COLOR_WHITE)
        
        self.required = required
        self.error_label = None
        
        # Label
        label_text = f"{label} *" if required else label
        tk.Label(
            self,
            text=label_text,
            bg=Config.COLOR_WHITE,
            font=Config.FONT_BODY,
            fg=Config.COLOR_TEXT
        ).pack(anchor="w")
        
        # Combobox
        self.combo = ttk.Combobox(
            self,
            width=width-3,
            state="readonly",
            font=Config.FONT_BODY
        )
        self.combo.pack(pady=(0, 5), fill="x")
        
        if options:
            self.set_options(options)
    
    def set_options(self, options):
        """Define as opções do combo."""
        self.combo['values'] = options
        if options:
            self.combo.current(0)
    
    def get(self):
        """Retorna o valor selecionado."""
        return self.combo.get()
    
    def set(self, value):
        """Define o valor selecionado."""
        self.combo.set(value)
    
    def get_index(self):
        """Retorna o índice selecionado."""
        return self.combo.current()
    
    def set_index(self, index):
        """Define por índice."""
        self.combo.current(index)
    
    def show_error(self, message):
        """Mostra erro."""
        if self.error_label:
            self.error_label.destroy()
        
        self.error_label = tk.Label(
            self,
            text=f"⚠ {message}",
            bg=Config.COLOR_WHITE,
            fg=Config.COLOR_SECONDARY,
            font=Config.FONT_SMALL
        )
        self.error_label.pack(anchor="w")
    
    def clear_error(self):
        """Remove erro."""
        if self.error_label:
            self.error_label.destroy()
            self.error_label = None
    
    def validate(self):
        """Valida o campo."""
        self.clear_error()
        if self.required and not self.get():
            self.show_error("Selecione uma opção")
            return False
        return True
