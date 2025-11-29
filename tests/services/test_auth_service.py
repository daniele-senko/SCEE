"""Testes para o AuthService."""
import pytest
from src.services.auth_service import AuthService
from src.repositories.user_repository import UsuarioRepository


class TestAuthService:
    """Testes do serviço de autenticação."""
    
    def test_login_admin_sucesso(self, db_connection, sample_admin):
        """Testa login de administrador com credenciais corretas."""
        auth = AuthService()
        
        resultado = auth.login(sample_admin["email"], sample_admin["senha"])
        
        assert resultado is True
        assert auth.get_usuario_atual() is not None
        assert auth.get_usuario_atual().email == sample_admin["email"]
    
    def test_login_cliente_sucesso(self, db_connection, sample_client):
        """Testa login de cliente com credenciais corretas."""
        auth = AuthService()
        
        resultado = auth.login(sample_client["email"], sample_client["senha"])
        
        assert resultado is True
        assert auth.get_usuario_atual() is not None
        assert auth.get_usuario_atual().email == sample_client["email"]
    
    def test_login_senha_incorreta(self, db_connection, sample_admin):
        """Testa login com senha incorreta."""
        auth = AuthService()
        
        resultado = auth.login(sample_admin["email"], "senha_errada")
        
        assert resultado is False
        assert auth.get_usuario_atual() is None
    
    def test_login_email_inexistente(self, db_connection):
        """Testa login com email que não existe."""
        auth = AuthService()
        
        resultado = auth.login("naoexiste@email.com", "qualquer_senha")
        
        assert resultado is False
        assert auth.get_usuario_atual() is None
    
    def test_logout(self, db_connection, sample_admin):
        """Testa logout do usuário."""
        auth = AuthService()
        
        # Faz login
        auth.login(sample_admin["email"], sample_admin["senha"])
        assert auth.get_usuario_atual() is not None
        
        # Faz logout
        auth.logout()
        assert auth.get_usuario_atual() is None
