import tkinter as tk
from tkinter import messagebox
from src.config.settings import Config
from src.services.auth_service import AuthService

class LoginView(tk.Frame):
    """
    Tela de Login do Cliente.
    Herda de tk.Frame para ser embutida na MainWindow.
    """

    def __init__(self, parent, controller):
        """
        :param parent: O container pai (onde esse frame ficará).
        :param controller: A MainWindow (para poder mudar de tela).
        """
        super().__init__(parent, bg=Config.COLOR_BG)
        self.controller = controller
        self.auth_service = AuthService() # Instancia a lógica

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
            text="Bem-vindo ao SCEE", 
            font=Config.FONT_TITLE,
            bg=Config.COLOR_WHITE, 
            fg=Config.COLOR_PRIMARY
        ).pack(pady=(0, 20))

        # Campo E-mail
        tk.Label(card, text="E-mail", font=Config.FONT_BODY, bg=Config.COLOR_WHITE, fg=Config.COLOR_TEXT).pack(anchor="w")
        self.entry_email = tk.Entry(card, font=Config.FONT_BODY, width=30)
        self.entry_email.pack(pady=(0, 15))

        # Campo Senha
        tk.Label(card, text="Senha", font=Config.FONT_BODY, bg=Config.COLOR_WHITE, fg=Config.COLOR_TEXT).pack(anchor="w")
        self.entry_senha = tk.Entry(card, font=Config.FONT_BODY, width=30, show="*")
        self.entry_senha.pack(pady=(0, 20))

        # Botão Entrar
        btn_login = tk.Button(
            card, 
            text="ENTRAR", 
            font=Config.FONT_HEADER,
            bg=Config.COLOR_PRIMARY, 
            fg="white",
            width=20,
            cursor="hand2",
            command=self._handle_login
        )
        btn_login.pack(pady=10)

        # Link Cadastrar
        btn_register = tk.Label(
            card, 
            text="Não tem conta? Cadastre-se", 
            font=Config.FONT_SMALL,
            bg=Config.COLOR_WHITE, 
            fg=Config.COLOR_ACCENT,
            cursor="hand2"
        )
        btn_register.pack(pady=5)
        # Evento de clique no label
        btn_register.bind("<Button-1>", lambda e: self.controller.show_view("RegisterView"))

    def _handle_login(self):
        email = self.entry_email.get()
        senha = self.entry_senha.get()

        if not email or not senha:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return

        if self.auth_service.login(email, senha):
            user = self.auth_service.get_usuario_atual()
            
            messagebox.showinfo("Sucesso", f"Bem-vindo, {user.nome}!")
            
            # --- Lógica de Redirecionamento ---
            # Verifica se é uma instância de Administrador (Polimorfismo)
            # O atributo 'tipo' vem do banco como string 'admin' ou 'cliente'
            
            # Opção A: Se usarmos o atributo 'tipo' que vem do banco (mais seguro)
            # Supondo que seu objeto user tenha user.tipo ou user.is_admin()
            
            # Opção B: Verificação de Classe (Funciona se o Repository instanciou a classe certa)
            from src.models.users.admin_model import Administrador
            
            if isinstance(user, Administrador):
                print(">> Redirecionando para Painel Admin")
                self.controller.show_view("AdminDashboard", data=user)
            else:
                print(">> Redirecionando para Loja Cliente")
                self.controller.show_view("HomeView", data=user)
            # --------------------------------------------------
            
        else:
            messagebox.showerror("Erro", "E-mail ou senha inválidos.")