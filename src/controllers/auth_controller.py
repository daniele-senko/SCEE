"""
AuthController - Controlador de Autenticação
============================================

Gerencia autenticação, registro e logout de usuários.
"""
from typing import Dict, Any
from src.controllers.base_controller import BaseController
from src.services.auth_service import AuthService
from src.repositories.user_repository import UsuarioRepository
from src.models.users.client_model import Cliente
from src.models.users.admin_model import Administrador
from src.utils.security.password_hasher import PasswordHasher
import re


class AuthController(BaseController):
    """
    Controller para operações de autenticação.
    
    Métodos:
    - login(): Autentica usuário
    - logout(): Desconecta usuário
    - register_client(): Registra novo cliente
    """
    
    def __init__(self, main_window):
        super().__init__(main_window)
        self.auth_service = AuthService()
        self.user_repository = UsuarioRepository()
    
    def login(self, email: str, senha: str) -> Dict[str, Any]:
        """
        Processa login do usuário.
        
        Args:
            email: Email do usuário
            senha: Senha em texto plano
            
        Returns:
            Dicionário com success, message e data (usuário)
        """
        # Validações básicas
        error = self._validate_not_empty(email, "Email")
        if error:
            return self._error_response(error)
        
        error = self._validate_not_empty(senha, "Senha")
        if error:
            return self._error_response(error)
        
        # Validar formato de email
        if not self._validate_email_format(email):
            return self._error_response("Email inválido")
        
        # Tentar autenticar
        try:
            if self.auth_service.login(email, senha):
                usuario = self.auth_service.get_usuario_atual()
                
                # Decidir navegação baseada no tipo de usuário
                if isinstance(usuario, Administrador):
                    self.navigate_to('AdminDashboard', usuario)
                else:
                    self.navigate_to('HomeView', usuario)
                
                return self._success_response(
                    f'Bem-vindo, {usuario.nome}!',
                    usuario
                )
            else:
                return self._error_response('Email ou senha incorretos')
        
        except Exception as e:
            return self._error_response(
                'Erro ao processar login',
                e
            )
    
    def logout(self) -> Dict[str, Any]:
        """
        Desconecta o usuário atual.
        
        Returns:
            Dicionário com success e message
        """
        try:
            self.auth_service.logout()
            self.navigate_to('LoginView')
            return self._success_response('Logout realizado com sucesso')
        
        except Exception as e:
            return self._error_response(
                'Erro ao processar logout',
                e
            )
    
    def register_client(
        self,
        nome: str,
        email: str,
        cpf: str,
        senha: str,
        confirmar_senha: str
    ) -> Dict[str, Any]:
        """
        Registra novo cliente.
        
        Args:
            nome: Nome completo
            email: Email
            cpf: CPF (apenas números)
            senha: Senha
            confirmar_senha: Confirmação de senha
            
        Returns:
            Dicionário com success, message e data (cliente)
        """
        # Validações básicas
        validations = [
            (nome, "Nome"),
            (email, "Email"),
            (cpf, "CPF"),
            (senha, "Senha"),
            (confirmar_senha, "Confirmação de senha")
        ]
        
        for value, field in validations:
            error = self._validate_not_empty(value, field)
            if error:
                return self._error_response(error)
        
        # Validar tamanho mínimo do nome
        error = self._validate_min_length(nome, "Nome", 3)
        if error:
            return self._error_response(error)
        
        # Validar formato de email
        if not self._validate_email_format(email):
            return self._error_response("Email inválido")
        
        # Validar CPF
        if not self._validate_cpf(cpf):
            return self._error_response("CPF inválido")
        
        # Validar senha
        error = self._validate_min_length(senha, "Senha", 6)
        if error:
            return self._error_response(error)
        
        # Validar confirmação de senha
        if senha != confirmar_senha:
            return self._error_response("Senhas não coincidem")
        
        # Verificar se email já existe
        try:
            usuario_existente = self.user_repository.buscar_por_email(email)
            if usuario_existente:
                return self._error_response("Email já cadastrado")
        except Exception as e:
            return self._error_response("Erro ao verificar email", e)
        
        # Criar novo cliente
        try:
            senha_hash = PasswordHasher.hash_password(senha)
            cliente = Cliente(nome, email, cpf, senha_hash)
            
            # Salvar no banco
            cliente_salvo = self.user_repository.salvar(cliente)
            
            # Auto-login após registro
            self.auth_service.login(email, senha)
            
            # Navegar para home
            self.navigate_to('HomeView', cliente_salvo)
            
            return self._success_response(
                'Cadastro realizado com sucesso!',
                cliente_salvo
            )
        
        except Exception as e:
            return self._error_response(
                'Erro ao cadastrar cliente',
                e
            )
    
    def _validate_email_format(self, email: str) -> bool:
        """
        Valida formato de email.
        
        Args:
            email: Email a validar
            
        Returns:
            True se válido, False caso contrário
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def _validate_cpf(self, cpf: str) -> bool:
        """
        Valida formato básico de CPF (11 dígitos).
        
        Args:
            cpf: CPF a validar
            
        Returns:
            True se válido, False caso contrário
        """
        # Remove caracteres não numéricos
        cpf_numeros = re.sub(r'\D', '', cpf)
        
        # Verifica se tem 11 dígitos
        if len(cpf_numeros) != 11:
            return False
        
        # Verifica se não são todos iguais (000.000.000-00, 111.111.111-11, etc.)
        if cpf_numeros == cpf_numeros[0] * 11:
            return False
        
        return True
