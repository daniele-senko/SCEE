from typing import Optional
from src.models.users.user_model import Usuario
from src.repositories.user_repository import UsuarioRepository
from src.utils.security.password_hasher import PasswordHasher

class AuthService:
    """
    Serviço responsável pela lógica de autenticação.
    Faz a ponte entre a Tela de Login e o Banco de Dados.
    """

    def __init__(self):
        self.repo = UsuarioRepository()
        self.usuario_logado: Optional[Usuario] = None

    def login(self, email: str, senha_plana: str) -> bool:
        """
        Tenta autenticar um usuário.
        :return: True se sucesso, False se falhar.
        """
        # 1. Busca o usuário no banco pelo email
        usuario = self.repo.buscar_por_email(email)
        
        if not usuario:
            return False
            
        # 2. Verifica a senha usando o Hasher
        if PasswordHasher.verify_password(usuario.senha_hash, senha_plana):
            self.usuario_logado = usuario
            return True
            
        return False

    def logout(self):
        self.usuario_logado = None

    def get_usuario_atual(self):
        return self.usuario_logado