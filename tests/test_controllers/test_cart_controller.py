"""
Testes para CartController
===========================

Testa operações de carrinho de compras.
"""
import pytest
from unittest.mock import Mock, patch
from src.controllers.cart_controller import CartController


@pytest.fixture
def mock_main_window():
    """Mock da MainWindow."""
    window = Mock()
    window.show_view = Mock()
    return window


@pytest.fixture
def controller(mock_main_window):
    """Fixture do CartController."""
    ctrl = CartController(mock_main_window)
    ctrl.set_current_user(1)  # Define usuário logado
    return ctrl


class TestCartControllerAddItem:
    """Testes de adicionar item ao carrinho."""
    
    def test_add_to_cart_sem_usuario(self, mock_main_window):
        """Deve falhar sem usuário logado."""
        controller = CartController(mock_main_window)
        result = controller.add_to_cart(1, 2)
        
        assert not result['success']
        assert 'não autenticado' in result['message']
    
    def test_add_to_cart_quantidade_zero(self, controller):
        """Deve falhar com quantidade zero."""
        result = controller.add_to_cart(1, 0)
        
        assert not result['success']
        assert 'maior que zero' in result['message']
    
    def test_add_to_cart_quantidade_negativa(self, controller):
        """Deve falhar com quantidade negativa."""
        result = controller.add_to_cart(1, -1)
        
        assert not result['success']
        assert 'maior que zero' in result['message']
    
    def test_add_to_cart_sucesso(self, controller):
        """Deve adicionar item com sucesso."""
        item = {
            'id': 1,
            'carrinho_id': 1,
            'produto_id': 1,
            'quantidade': 2,
            'preco_unitario': 100.00
        }
        
        with patch.object(controller.cart_service, 'adicionar_item', return_value=item):
            result = controller.add_to_cart(1, 2)
        
        assert result['success']
        assert 'adicionado' in result['message']
        assert result['data'] == item
    
    def test_add_to_cart_estoque_insuficiente(self, controller):
        """Deve tratar erro de estoque insuficiente."""
        with patch.object(controller.cart_service, 'adicionar_item', 
                         side_effect=Exception("Estoque insuficiente")):
            result = controller.add_to_cart(1, 10)
        
        assert not result['success']
        assert 'sem estoque' in result['message']
    
    def test_add_to_cart_produto_nao_encontrado(self, controller):
        """Deve tratar produto não encontrado."""
        with patch.object(controller.cart_service, 'adicionar_item',
                         side_effect=Exception("Produto não encontrado")):
            result = controller.add_to_cart(999, 1)
        
        assert not result['success']
        assert 'não disponível' in result['message']


class TestCartControllerRemoveItem:
    """Testes de remover item do carrinho."""
    
    def test_remove_from_cart_sem_usuario(self, mock_main_window):
        """Deve falhar sem usuário logado."""
        controller = CartController(mock_main_window)
        result = controller.remove_from_cart(1)
        
        assert not result['success']
    
    def test_remove_from_cart_sucesso(self, controller):
        """Deve remover item com sucesso."""
        with patch.object(controller.cart_service, 'remover_item'):
            result = controller.remove_from_cart(1)
        
        assert result['success']
        assert 'removido' in result['message']
    
    def test_remove_from_cart_exception(self, controller):
        """Deve tratar exceção ao remover."""
        with patch.object(controller.cart_service, 'remover_item',
                         side_effect=Exception("Error")):
            result = controller.remove_from_cart(1)
        
        assert not result['success']


class TestCartControllerUpdateQuantity:
    """Testes de atualizar quantidade."""
    
    def test_update_quantity_sem_usuario(self, mock_main_window):
        """Deve falhar sem usuário logado."""
        controller = CartController(mock_main_window)
        result = controller.update_quantity(1, 5)
        
        assert not result['success']
    
    def test_update_quantity_negativa(self, controller):
        """Deve falhar com quantidade negativa."""
        result = controller.update_quantity(1, -1)
        
        assert not result['success']
        assert 'inválida' in result['message']
    
    def test_update_quantity_zero_remove_item(self, controller):
        """Quantidade zero deve remover item."""
        with patch.object(controller.cart_service, 'remover_item'):
            result = controller.update_quantity(1, 0)
        
        assert result['success']
        assert 'removido' in result['message']
    
    def test_update_quantity_sucesso(self, controller):
        """Deve atualizar quantidade com sucesso."""
        with patch.object(controller.cart_service, 'atualizar_quantidade'):
            result = controller.update_quantity(1, 3)
        
        assert result['success']
        assert 'atualizada' in result['message']
    
    def test_update_quantity_estoque_insuficiente(self, controller):
        """Deve tratar estoque insuficiente."""
        with patch.object(controller.cart_service, 'atualizar_quantidade',
                         side_effect=Exception("Estoque insuficiente")):
            result = controller.update_quantity(1, 100)
        
        assert not result['success']
        assert 'Estoque' in result['message']


class TestCartControllerClear:
    """Testes de limpar carrinho."""
    
    def test_clear_cart_sem_usuario(self, mock_main_window):
        """Deve falhar sem usuário logado."""
        controller = CartController(mock_main_window)
        result = controller.clear_cart()
        
        assert not result['success']
    
    def test_clear_cart_sucesso(self, controller):
        """Deve limpar carrinho com sucesso."""
        carrinho = {'id': 1, 'usuario_id': 1}
        
        with patch.object(controller.cart_service, 'obter_ou_criar_carrinho', return_value=carrinho):
            with patch.object(controller.cart_service, 'limpar_carrinho'):
                result = controller.clear_cart()
        
        assert result['success']
        assert 'limpo' in result['message']


class TestCartControllerGetCart:
    """Testes de obter carrinho."""
    
    def test_get_cart_sem_usuario(self, mock_main_window):
        """Deve falhar sem usuário logado."""
        controller = CartController(mock_main_window)
        result = controller.get_cart()
        
        assert not result['success']
    
    def test_get_cart_vazio(self, controller):
        """Deve retornar carrinho vazio."""
        carrinho = {'id': 1, 'usuario_id': 1}
        
        with patch.object(controller.cart_service, 'obter_ou_criar_carrinho', return_value=carrinho):
            with patch.object(controller.cart_service, 'listar_itens', return_value=[]):
                with patch.object(controller.cart_service, 'calcular_total', return_value=0.0):
                    result = controller.get_cart()
        
        assert result['success']
        assert result['data']['quantidade_itens'] == 0
        assert result['data']['total'] == 0.0
    
    def test_get_cart_com_itens(self, controller):
        """Deve retornar carrinho com itens."""
        carrinho = {'id': 1, 'usuario_id': 1}
        itens = [
            {'id': 1, 'produto_id': 1, 'quantidade': 2, 'preco_unitario': 100.00},
            {'id': 2, 'produto_id': 2, 'quantidade': 1, 'preco_unitario': 50.00}
        ]
        total = 250.00
        
        with patch.object(controller.cart_service, 'obter_ou_criar_carrinho', return_value=carrinho):
            with patch.object(controller.cart_service, 'listar_itens', return_value=itens):
                with patch.object(controller.cart_service, 'calcular_total', return_value=total):
                    result = controller.get_cart()
        
        assert result['success']
        assert result['data']['quantidade_itens'] == 2
        assert result['data']['total'] == 250.00


class TestCartControllerNavigation:
    """Testes de navegação."""
    
    def test_view_cart(self, controller, mock_main_window):
        """Deve navegar para tela do carrinho."""
        carrinho = {'id': 1, 'usuario_id': 1}
        
        with patch.object(controller.cart_service, 'obter_ou_criar_carrinho', return_value=carrinho):
            with patch.object(controller.cart_service, 'listar_itens', return_value=[]):
                with patch.object(controller.cart_service, 'calcular_total', return_value=0.0):
                    result = controller.view_cart()
        
        assert result['success']
        mock_main_window.show_view.assert_called_once()
    
    def test_proceed_to_checkout_carrinho_vazio(self, controller):
        """Deve falhar ao prosseguir com carrinho vazio."""
        carrinho = {'id': 1, 'usuario_id': 1}
        
        with patch.object(controller.cart_service, 'obter_ou_criar_carrinho', return_value=carrinho):
            with patch.object(controller.cart_service, 'listar_itens', return_value=[]):
                with patch.object(controller.cart_service, 'calcular_total', return_value=0.0):
                    result = controller.proceed_to_checkout()
        
        assert not result['success']
        assert 'vazio' in result['message']
    
    def test_proceed_to_checkout_sucesso(self, controller, mock_main_window):
        """Deve prosseguir para checkout com itens."""
        carrinho = {'id': 1, 'usuario_id': 1}
        itens = [{'id': 1, 'produto_id': 1, 'quantidade': 1}]
        
        with patch.object(controller.cart_service, 'obter_ou_criar_carrinho', return_value=carrinho):
            with patch.object(controller.cart_service, 'listar_itens', return_value=itens):
                with patch.object(controller.cart_service, 'calcular_total', return_value=100.0):
                    result = controller.proceed_to_checkout()
        
        assert result['success']
        # Verifica que navegou para CheckoutView
        assert mock_main_window.show_view.call_count == 1
        assert mock_main_window.show_view.call_args[0][0] == 'CheckoutView'
