"""
Testes para AuthController
===========================

Testa operações de autenticação, registro e logout.
"""
import pytest
from unittest.mock import Mock, MagicMock, patch
from src.controllers.auth_controller import AuthController
from src.models.users.client_model import Cliente
from src.models.users.admin_model import Administrador


@pytest.fixture
def mock_main_window():
    """Mock da MainWindow."""
    window = Mock()
    window.show_view = Mock()
    return window


@pytest.fixture
def controller(mock_main_window):
    """Fixture do AuthController."""
    return AuthController(mock_main_window)


class TestAuthControllerLogin:
    """Testes de login."""
    
    def test_login_campos_vazios(self, controller):
        """Deve falhar com campos vazios."""
        result = controller.login("", "")
        
        assert not result['success']
        assert 'Email' in result['message']
    
    def test_login_email_invalido(self, controller):
        """Deve falhar com email inválido."""
        result = controller.login("email-invalido", "senha123")
        
        assert not result['success']
        assert 'Email inválido' in result['message']
    
    def test_login_credenciais_incorretas(self, controller):
        """Deve falhar com credenciais incorretas."""
        with patch.object(controller.auth_service, 'login', return_value=False):
            result = controller.login("test@example.com", "senha_errada")
        
        assert not result['success']
        assert 'incorretos' in result['message']
    
    def test_login_cliente_sucesso(self, controller, mock_main_window):
        """Deve logar cliente com sucesso."""
        # Mock cliente
        cliente = Cliente("João", "joao@email.com", "12345678900", "hash")
        cliente._id = 1
        
        with patch.object(controller.auth_service, 'login', return_value=True):
            with patch.object(controller.auth_service, 'get_usuario_atual', return_value=cliente):
                result = controller.login("joao@email.com", "senha123")
        
        assert result['success']
        assert 'Bem-vindo' in result['message']
        assert result['data'] == cliente
        mock_main_window.show_view.assert_called_once_with('HomeView', cliente)
    
    def test_login_admin_sucesso(self, controller, mock_main_window):
        """Deve logar admin e redirecionar para dashboard."""
        # Mock admin
        admin = Administrador("Admin", "admin@scee.com", "hash", "gerente")
        admin._id = 2
        
        with patch.object(controller.auth_service, 'login', return_value=True):
            with patch.object(controller.auth_service, 'get_usuario_atual', return_value=admin):
                result = controller.login("admin@scee.com", "admin123")
        
        assert result['success']
        mock_main_window.show_view.assert_called_once_with('AdminDashboard', admin)
    
    def test_login_exception(self, controller):
        """Deve tratar exceção no login."""
        with patch.object(controller.auth_service, 'login', side_effect=Exception("DB Error")):
            result = controller.login("test@example.com", "senha123")
        
        assert not result['success']
        assert 'Erro ao processar login' in result['message']


class TestAuthControllerLogout:
    """Testes de logout."""
    
    def test_logout_sucesso(self, controller, mock_main_window):
        """Deve fazer logout com sucesso."""
        with patch.object(controller.auth_service, 'logout'):
            result = controller.logout()
        
        assert result['success']
        assert 'sucesso' in result['message']
        mock_main_window.show_view.assert_called_once_with('LoginView', None)
    
    def test_logout_exception(self, controller):
        """Deve tratar exceção no logout."""
        with patch.object(controller.auth_service, 'logout', side_effect=Exception("Error")):
            result = controller.logout()
        
        assert not result['success']


class TestAuthControllerRegister:
    """Testes de registro de cliente."""
    
    def test_register_campos_vazios(self, controller):
        """Deve falhar com campos vazios."""
        result = controller.register_client("", "", "", "", "")
        
        assert not result['success']
        assert 'Nome' in result['message'] or 'Email' in result['message']
    
    def test_register_nome_muito_curto(self, controller):
        """Deve falhar com nome muito curto."""
        result = controller.register_client(
            "Jo", "joao@email.com", "12345678900", "senha123", "senha123"
        )
        
        assert not result['success']
        assert 'Nome' in result['message']
    
    def test_register_email_invalido(self, controller):
        """Deve falhar com email inválido."""
        result = controller.register_client(
            "João Silva", "email-invalido", "12345678900", "senha123", "senha123"
        )
        
        assert not result['success']
        assert 'Email inválido' in result['message']
    
    def test_register_cpf_invalido(self, controller):
        """Deve falhar com CPF inválido."""
        result = controller.register_client(
            "João Silva", "joao@email.com", "123", "senha123", "senha123"
        )
        
        assert not result['success']
        assert 'CPF inválido' in result['message']
    
    def test_register_senha_muito_curta(self, controller):
        """Deve falhar com senha muito curta."""
        result = controller.register_client(
            "João Silva", "joao@email.com", "12345678900", "123", "123"
        )
        
        assert not result['success']
        assert 'Senha' in result['message']
    
    def test_register_senhas_nao_coincidem(self, controller):
        """Deve falhar quando senhas não coincidem."""
        result = controller.register_client(
            "João Silva", "joao@email.com", "12345678900", "senha123", "senha456"
        )
        
        assert not result['success']
        assert 'não coincidem' in result['message']
    
    def test_register_email_ja_existe(self, controller):
        """Deve falhar quando email já está cadastrado."""
        cliente_existente = Cliente("Outro", "joao@email.com", "98765432100", "hash")
        
        with patch.object(controller.user_repository, 'buscar_por_email', return_value=cliente_existente):
            result = controller.register_client(
                "João Silva", "joao@email.com", "12345678900", "senha123", "senha123"
            )
        
        assert not result['success']
        assert 'já cadastrado' in result['message']
    
    def test_register_sucesso(self, controller, mock_main_window):
        """Deve registrar cliente com sucesso."""
        cliente = Cliente("João Silva", "joao@email.com", "12345678900", "hash")
        cliente._id = 1
        
        with patch.object(controller.user_repository, 'buscar_por_email', return_value=None):
            with patch.object(controller.user_repository, 'salvar', return_value=cliente):
                with patch.object(controller.auth_service, 'login', return_value=True):
                    result = controller.register_client(
                        "João Silva", "joao@email.com", "12345678900", "senha123", "senha123"
                    )
        
        assert result['success']
        assert 'sucesso' in result['message']
        mock_main_window.show_view.assert_called_once_with('HomeView', cliente)


class TestAuthControllerValidacoes:
    """Testes de validações auxiliares."""
    
    def test_validate_email_format_valido(self, controller):
        """Deve validar email válido."""
        assert controller._validate_email_format("test@example.com")
        assert controller._validate_email_format("user.name@domain.co.uk")
    
    def test_validate_email_format_invalido(self, controller):
        """Deve rejeitar email inválido."""
        assert not controller._validate_email_format("email-sem-arroba")
        assert not controller._validate_email_format("@domain.com")
        assert not controller._validate_email_format("user@")
    
    def test_validate_cpf_valido(self, controller):
        """Deve validar CPF com 11 dígitos."""
        assert controller._validate_cpf("12345678901")
        assert controller._validate_cpf("123.456.789-01")  # Com formatação
    
    def test_validate_cpf_invalido(self, controller):
        """Deve rejeitar CPF inválido."""
        assert not controller._validate_cpf("123")  # Muito curto
        assert not controller._validate_cpf("00000000000")  # Todos iguais
        assert not controller._validate_cpf("11111111111")  # Todos iguais
