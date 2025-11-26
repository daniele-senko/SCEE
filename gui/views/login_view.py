"""
Tela de Login - SCEE
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging

from src.services.auth_service import AuthService
from repositories.usuario_repository import UsuarioRepository
from config.database import get_connection

logger = logging.getLogger(__name__)


class LoginView:
    """Tela de login da aplicação"""
    
    def __init__(self, parent, on_success_callback):
        """
        Inicializa a view de login
        
        Args:
            parent: Widget pai (janela principal)
            on_success_callback: Função chamada quando login é bem-sucedido
        """
        self.parent = parent
        self.on_success_callback = on_success_callback
        
        # Inicializar serviços
        self.usuario_repo = UsuarioRepository(get_connection)
        self.auth_service = AuthService(self.usuario_repo)
        
        # Criar interface
        self.create_widgets()
        
    def create_widgets(self):
        """Cria os widgets da tela de login"""
        
        # Container principal
        self.main_frame = tk.Frame(self.parent, bg='#f8fafc')
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Container central
        center_frame = tk.Frame(self.main_frame, bg='#ffffff', padx=50, pady=50)
        center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Logo/Título
        title_label = tk.Label(
            center_frame,
            text="🛒 SCEE",
            font=('Arial', 32, 'bold'),
            bg='#ffffff',
            fg='#2563eb'
        )
        title_label.pack(pady=(0, 10))
        
        subtitle_label = tk.Label(
            center_frame,
            text="Sistema de Comércio Eletrônico",
            font=('Arial', 14),
            bg='#ffffff',
            fg='#64748b'
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Frame do formulário
        form_frame = tk.Frame(center_frame, bg='#ffffff')
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Email
        email_label = tk.Label(
            form_frame,
            text="Email:",
            font=('Arial', 11),
            bg='#ffffff',
            fg='#1e293b'
        )
        email_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.email_entry = tk.Entry(
            form_frame,
            font=('Arial', 12),
            width=30,
            relief=tk.SOLID,
            borderwidth=1
        )
        self.email_entry.pack(pady=(0, 15), ipady=8)
        self.email_entry.focus()
        
        # Senha
        password_label = tk.Label(
            form_frame,
            text="Senha:",
            font=('Arial', 11),
            bg='#ffffff',
            fg='#1e293b'
        )
        password_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.password_entry = tk.Entry(
            form_frame,
            font=('Arial', 12),
            width=30,
            show='●',
            relief=tk.SOLID,
            borderwidth=1
        )
        self.password_entry.pack(pady=(0, 25), ipady=8)
        
        # Bind Enter key
        self.email_entry.bind('<Return>', lambda e: self.password_entry.focus())
        self.password_entry.bind('<Return>', lambda e: self.login())
        
        # Botão de login
        login_button = tk.Button(
            form_frame,
            text="Entrar",
            font=('Arial', 12, 'bold'),
            bg='#2563eb',
            fg='#ffffff',
            activebackground='#1d4ed8',
            activeforeground='#ffffff',
            relief=tk.FLAT,
            cursor='hand2',
            command=self.login,
            width=30,
            height=2
        )
        login_button.pack(pady=(0, 15))
        
        # Link para registro
        register_frame = tk.Frame(form_frame, bg='#ffffff')
        register_frame.pack()
        
        register_text = tk.Label(
            register_frame,
            text="Não tem uma conta? ",
            font=('Arial', 10),
            bg='#ffffff',
            fg='#64748b'
        )
        register_text.pack(side=tk.LEFT)
        
        register_link = tk.Label(
            register_frame,
            text="Registre-se",
            font=('Arial', 10, 'underline'),
            bg='#ffffff',
            fg='#2563eb',
            cursor='hand2'
        )
        register_link.pack(side=tk.LEFT)
        register_link.bind('<Button-1>', lambda e: self.show_register())
        
        # Credenciais de teste (remover em produção)
        test_info = tk.Label(
            center_frame,
            text="👤 Teste: admin@scee.com / admin123",
            font=('Arial', 9, 'italic'),
            bg='#ffffff',
            fg='#94a3b8',
            pady=20
        )
        test_info.pack()
        
    def login(self):
        """Realiza o login"""
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        
        # Validar campos
        if not email:
            messagebox.showwarning("Atenção", "Por favor, informe o email.")
            self.email_entry.focus()
            return
            
        if not password:
            messagebox.showwarning("Atenção", "Por favor, informe a senha.")
            self.password_entry.focus()
            return
        
        try:
            # Tentar fazer login
            logger.info(f"Tentando login para: {email}")
            user = self.auth_service.login(email, password)
            
            if user:
                logger.info(f"Login bem-sucedido: {email}")
                messagebox.showinfo("Sucesso", f"Bem-vindo, {user['nome']}!")
                
                # Chamar callback de sucesso
                if self.on_success_callback:
                    self.on_success_callback(user)
            else:
                logger.warning(f"Login falhou para: {email}")
                messagebox.showerror("Erro", "Email ou senha inválidos.")
                self.password_entry.delete(0, tk.END)
                self.password_entry.focus()
                
        except Exception as e:
            logger.error(f"Erro ao fazer login: {e}", exc_info=True)
            messagebox.showerror("Erro", f"Erro ao fazer login:\n{str(e)}")
            
    def show_register(self):
        """Mostra a tela de registro"""
        # TODO: Implementar tela de registro
        messagebox.showinfo("Em desenvolvimento", "Tela de registro em desenvolvimento.")
