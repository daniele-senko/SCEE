"""Testes para o UserRepository."""
import pytest
from src.repositories.user_repository import UsuarioRepository
from src.models.users.client_model import Cliente
from src.models.users.admin_model import Administrador
from src.utils.security.password_hasher import PasswordHasher


class TestUsuarioRepository:
    """Testes do repositório de usuários."""
    
    def test_buscar_admin_por_email(self, db_connection, sample_admin):
        """Testa busca de administrador por email."""
        repo = UsuarioRepository()
        
        usuario = repo.buscar_por_email(sample_admin["email"])
        
        assert usuario is not None
        assert isinstance(usuario, Administrador)
        assert usuario.email == sample_admin["email"]
    
    def test_buscar_cliente_por_email(self, db_connection, sample_client):
        """Testa busca de cliente por email."""
        repo = UsuarioRepository()
        
        usuario = repo.buscar_por_email(sample_client["email"])
        
        assert usuario is not None
        assert isinstance(usuario, Cliente)
        assert usuario.email == sample_client["email"]
        assert usuario.cpf == sample_client["cpf"]
    
    def test_salvar_novo_cliente(self, db_connection):
        """Testa salvamento de novo cliente."""
        repo = UsuarioRepository()
        senha_hash = PasswordHasher.hash_password("senha123")
        
        novo_cliente = Cliente(
            nome="Maria Santos",
            email="maria@email.com",
            cpf="987.654.321-00",
            senha_hash=senha_hash
        )
        
        resultado = repo.salvar(novo_cliente)
        
        assert resultado.id is not None
        assert resultado.email == "maria@email.com"
        
        # Verifica se pode buscar o cliente salvo
        cliente_buscado = repo.buscar_por_email("maria@email.com")
        assert cliente_buscado is not None
        assert cliente_buscado.cpf == "987.654.321-00"
    
    def test_listar_usuarios(self, db_connection):
        """Testa listagem de todos os usuários."""
        repo = UsuarioRepository()
        
        usuarios = repo.listar()
        
        assert len(usuarios) >= 2  # Pelo menos admin e cliente do seed
        assert any(isinstance(u, Administrador) for u in usuarios)
        assert any(isinstance(u, Cliente) for u in usuarios)
    
    def test_deletar_usuario(self, db_connection):
        """Testa deleção de usuário."""
        repo = UsuarioRepository()
        senha_hash = PasswordHasher.hash_password("senha123")
        
        # Cria usuário temporário
        temp_cliente = Cliente(
            nome="Temp User",
            email="temp@email.com",
            cpf="111.111.111-11",
            senha_hash=senha_hash
        )
        temp_cliente = repo.salvar(temp_cliente)
        
        # Deleta
        resultado = repo.deletar(temp_cliente.id)
        
        assert resultado is True
        
        # Verifica que não existe mais
        usuario_deletado = repo.buscar_por_id(temp_cliente.id)
        assert usuario_deletado is None
