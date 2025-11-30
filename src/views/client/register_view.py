import tkinter as tk
from tkinter import messagebox
from src.config.settings import Config
from src.controllers.auth_controller import AuthController


class RegisterView(tk.Frame):
    """
    Tela de Cadastro de Novos Clientes.
    Permite que visitantes criem uma conta no sistema.
    """

    def __init__(self, parent, controller):
        """
        :param parent: O container pai (onde esse frame ficará).
        :param controller: A MainWindow (para poder mudar de tela).
        """
        super().__init__(parent, bg=Config.COLOR_BG)
        self.controller = controller
        self.auth_controller = AuthController(controller)

        # Centraliza o conteúdo
        self.place(relx=0.5, rely=0.5, anchor="center")
        self.pack(fill="both", expand=True)

        self._setup_ui()

    def _setup_ui(self):
        """Constrói os Widgets da tela."""
        
        # Container Central (Card Branco)
        card = tk.Frame(self, bg=Config.COLOR_WHITE, padx=40, pady=40)
        card.place(relx=0.5, rely=0.5, anchor="center")

        # Título
        tk.Label(
            card, 
            text="Criar Nova Conta", 
            font=Config.FONT_TITLE,
            bg=Config.COLOR_WHITE, 
            fg=Config.COLOR_PRIMARY
        ).pack(pady=(0, 20))

        # Campo Nome Completo
        tk.Label(
            card, 
            text="Nome Completo", 
            font=Config.FONT_BODY, 
            bg=Config.COLOR_WHITE, 
            fg=Config.COLOR_TEXT
        ).pack(anchor="w")
        self.entry_nome = tk.Entry(card, font=Config.FONT_BODY, width=35)
        self.entry_nome.pack(pady=(0, 10))

        # Campo Email
        tk.Label(
            card, 
            text="E-mail", 
            font=Config.FONT_BODY, 
            bg=Config.COLOR_WHITE, 
            fg=Config.COLOR_TEXT
        ).pack(anchor="w")
        self.entry_email = tk.Entry(card, font=Config.FONT_BODY, width=35)
        self.entry_email.pack(pady=(0, 10))

        # Campo CPF
        tk.Label(
            card, 
            text="CPF (apenas números)", 
            font=Config.FONT_BODY, 
            bg=Config.COLOR_WHITE, 
            fg=Config.COLOR_TEXT
        ).pack(anchor="w")
        self.entry_cpf = tk.Entry(card, font=Config.FONT_BODY, width=35)
        self.entry_cpf.pack(pady=(0, 10))

        # Campo Telefone
        tk.Label(
            card, 
            text="Telefone (opcional - em desenvolvimento)", 
            font=Config.FONT_BODY, 
            bg=Config.COLOR_WHITE, 
            fg=Config.COLOR_TEXT_LIGHT
        ).pack(anchor="w")
        self.entry_telefone = tk.Entry(card, font=Config.FONT_BODY, width=35)
        self.entry_telefone.pack(pady=(0, 10))

        # Campo Senha
        tk.Label(
            card, 
            text="Senha (mínimo 6 caracteres)", 
            font=Config.FONT_BODY, 
            bg=Config.COLOR_WHITE, 
            fg=Config.COLOR_TEXT
        ).pack(anchor="w")
        self.entry_senha = tk.Entry(card, font=Config.FONT_BODY, width=35, show="*")
        self.entry_senha.pack(pady=(0, 10))

        # Campo Confirmar Senha
        tk.Label(
            card, 
            text="Confirmar Senha", 
            font=Config.FONT_BODY, 
            bg=Config.COLOR_WHITE, 
            fg=Config.COLOR_TEXT
        ).pack(anchor="w")
        self.entry_confirma_senha = tk.Entry(card, font=Config.FONT_BODY, width=35, show="*")
        self.entry_confirma_senha.pack(pady=(0, 20))

        # Botão Cadastrar
        btn_register = tk.Button(
            card, 
            text="CADASTRAR", 
            font=Config.FONT_HEADER,
            bg=Config.COLOR_PRIMARY, 
            fg="white",
            width=25,
            cursor="hand2",
            command=self._handle_register
        )
        btn_register.pack(pady=10)

        # Link Voltar para Login
        btn_back = tk.Label(
            card, 
            text="Já tem conta? Fazer login", 
            font=Config.FONT_SMALL,
            bg=Config.COLOR_WHITE, 
            fg=Config.COLOR_ACCENT,
            cursor="hand2"
        )
        btn_back.pack(pady=5)
        btn_back.bind("<Button-1>", lambda e: self.controller.show_view("LoginView"))

    def _handle_register(self):
        """Processa o cadastro do novo cliente."""
        
        # Coleta os dados do formulário
        nome = self.entry_nome.get().strip()
        email = self.entry_email.get().strip()
        cpf = self.entry_cpf.get().strip()
        telefone = self.entry_telefone.get().strip()
        senha = self.entry_senha.get()
        confirma_senha = self.entry_confirma_senha.get()

        # Validações básicas no frontend
        if not nome or not email or not cpf or not senha:
            messagebox.showwarning("Atenção", "Preencha os campos obrigatórios (nome, email, CPF e senha)!")
            return

        if len(senha) < 6:
            messagebox.showwarning("Atenção", "A senha deve ter no mínimo 6 caracteres!")
            return

        if senha != confirma_senha:
            messagebox.showerror("Erro", "As senhas não conferem!")
            return

        # Remove caracteres especiais do CPF
        cpf_numeros = ''.join(filter(str.isdigit, cpf))

        if len(cpf_numeros) != 11:
            messagebox.showwarning("Atenção", "CPF deve conter 11 dígitos!")
            return

        # Chama o controller para registrar
        resultado = self.auth_controller.register_client(
            nome=nome,
            email=email,
            cpf=cpf_numeros,
            senha=senha,
            confirmar_senha=confirma_senha
            # Nota: telefone não é usado no momento pois o modelo Cliente não suporta
        )

        # Processa a resposta
        if resultado['success']:
            messagebox.showinfo("Sucesso", resultado['message'])
            # Redireciona para login após cadastro bem-sucedido
            self.controller.show_view("LoginView")
        else:
            messagebox.showerror("Erro", resultado['message'])
