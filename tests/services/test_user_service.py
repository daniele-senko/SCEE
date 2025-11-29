"""Testes para o UsuarioService."""
import pytest
from src.services.user_service import (
    UsuarioService,
    UsuarioServiceError,
    UsuarioNaoEncontradoError,
    EmailInvalidoError,
    SenhaFracaError,
    PermissaoNegadaError
)
from src.repositories.user_repository import UsuarioRepository
from src.utils.security.password_hasher import PasswordHasher


class TestUsuarioService:
    """Testes do serviço de usuários."""
    
    def test_validar_nome_valido(self):
        """Testa validação de nome válido."""
        usuario_repo = UsuarioRepository()
        service = UsuarioService(usuario_repo)
        
        # Nome válido não deve lançar exceção
        try:
            service._validar_nome("João Silva")
            sucesso = True
        except:
            sucesso = False
        
        assert sucesso is True
    
    def test_validar_nome_muito_curto(self):
        """Testa validação de nome muito curto."""
        usuario_repo = UsuarioRepository()
        service = UsuarioService(usuario_repo)
        
        with pytest.raises(UsuarioServiceError, match="pelo menos"):
            service._validar_nome("Jo")
    
    def test_validar_email_valido(self):
        """Testa validação de email válido."""
        usuario_repo = UsuarioRepository()
        service = UsuarioService(usuario_repo)
        
        # Email válido não deve lançar exceção
        try:
            service._validar_email("teste@email.com")
            sucesso = True
        except:
            sucesso = False
        
        assert sucesso is True
    
    def test_validar_email_invalido(self):
        """Testa validação de email inválido."""
        usuario_repo = UsuarioRepository()
        service = UsuarioService(usuario_repo)
        
        with pytest.raises(EmailInvalidoError):
            service._validar_email("email-sem-arroba")
    
    def test_validar_senha_forte(self):
        """Testa validação de senha forte."""
        usuario_repo = UsuarioRepository()
        service = UsuarioService(usuario_repo)
        
        # Senha forte não deve lançar exceção
        try:
            service._validar_senha("SenhaForte123")
            sucesso = True
        except:
            sucesso = False
        
        assert sucesso is True
    
    def test_validar_senha_fraca_curta(self):
        """Testa validação de senha muito curta."""
        usuario_repo = UsuarioRepository()
        service = UsuarioService(usuario_repo)
        
        with pytest.raises(SenhaFracaError, match="pelo menos"):
            service._validar_senha("abc123")
    
    def test_validar_senha_sem_numero(self):
        """Testa validação de senha sem número."""
        usuario_repo = UsuarioRepository()
        service = UsuarioService(usuario_repo)
        
        with pytest.raises(SenhaFracaError, match="letra e um número"):
            service._validar_senha("SenhaSemNumero")
    
    def test_validar_senha_sem_letra(self):
        """Testa validação de senha sem letra."""
        usuario_repo = UsuarioRepository()
        service = UsuarioService(usuario_repo)
        
        with pytest.raises(SenhaFracaError, match="letra e um número"):
            service._validar_senha("12345678")

