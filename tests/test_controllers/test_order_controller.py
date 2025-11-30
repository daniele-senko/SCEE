"""
Testes para OrderController
============================

Testa operações de pedidos.
"""
import pytest
from unittest.mock import Mock, patch
from src.controllers.order_controller import OrderController


@pytest.fixture
def mock_main_window():
    """Mock da MainWindow."""
    window = Mock()
    window.show_view = Mock()
    return window


@pytest.fixture
def controller(mock_main_window):
    """Fixture do OrderController."""
    ctrl = OrderController(mock_main_window)
    ctrl.set_current_user(1)
    return ctrl


@pytest.fixture
def itens_pedido():
    """Itens de pedido mock."""
    return [
        {'produto_id': 1, 'quantidade': 2, 'preco_unitario': 100.00},
        {'produto_id': 2, 'quantidade': 1, 'preco_unitario': 50.00}
    ]


@pytest.fixture
def pedido_mock():
    """Pedido mock."""
    return {
        'id': 1,
        'usuario_id': 1,
        'endereco_id': 1,
        'status': 'PENDENTE',
        'subtotal': 250.00,
        'frete': 15.00,
        'total': 265.00,
        'tipo_pagamento': 'PIX'
    }


class TestOrderControllerCreateOrder:
    """Testes de criar pedido."""
    
    def test_create_order_sem_usuario(self, mock_main_window, itens_pedido):
        """Deve falhar sem usuário logado."""
        controller = OrderController(mock_main_window)
        result = controller.create_order(1, itens_pedido, 'PIX')
        
        assert not result['success']
        assert 'não autenticado' in result['message']
    
    def test_create_order_sem_itens(self, controller):
        """Deve falhar sem itens."""
        result = controller.create_order(1, [], 'PIX')
        
        assert not result['success']
        assert 'pelo menos um item' in result['message']
    
    def test_create_order_pagamento_invalido(self, controller, itens_pedido):
        """Deve falhar com tipo de pagamento inválido."""
        result = controller.create_order(1, itens_pedido, 'INVALIDO')
        
        assert not result['success']
        assert 'inválido' in result['message']
    
    def test_create_order_sucesso_pix(self, controller, itens_pedido, pedido_mock):
        """Deve criar pedido PIX com sucesso."""
        with patch.object(controller.order_service, 'criar_pedido', return_value=pedido_mock):
            result = controller.create_order(1, itens_pedido, 'PIX', 15.00)
        
        assert result['success']
        assert 'criado com sucesso' in result['message']
        assert '#1' in result['message']
        assert result['data'] == pedido_mock
    
    def test_create_order_sucesso_cartao(self, controller, itens_pedido, pedido_mock):
        """Deve criar pedido com cartão."""
        pedido_mock['tipo_pagamento'] = 'CARTAO'
        
        with patch.object(controller.order_service, 'criar_pedido', return_value=pedido_mock):
            result = controller.create_order(1, itens_pedido, 'CARTAO')
        
        assert result['success']
    
    def test_create_order_estoque_insuficiente(self, controller, itens_pedido):
        """Deve tratar estoque insuficiente."""
        with patch.object(controller.order_service, 'criar_pedido',
                         side_effect=Exception("Estoque insuficiente")):
            result = controller.create_order(1, itens_pedido, 'PIX')
        
        assert not result['success']
        assert 'sem estoque' in result['message']
    
    def test_create_order_endereco_invalido(self, controller, itens_pedido):
        """Deve tratar endereço inválido."""
        with patch.object(controller.order_service, 'criar_pedido',
                         side_effect=Exception("Endereço inválido")):
            result = controller.create_order(999, itens_pedido, 'PIX')
        
        assert not result['success']
        assert 'Endereço inválido' in result['message']


class TestOrderControllerGetMyOrders:
    """Testes de listar pedidos."""
    
    def test_get_my_orders_sem_usuario(self, mock_main_window):
        """Deve falhar sem usuário logado."""
        controller = OrderController(mock_main_window)
        result = controller.get_my_orders()
        
        assert not result['success']
    
    def test_get_my_orders_todos(self, controller, pedido_mock):
        """Deve listar todos os pedidos do usuário."""
        pedidos = [pedido_mock]
        
        with patch.object(controller.order_service, 'listar_pedidos_usuario', return_value=pedidos):
            result = controller.get_my_orders()
        
        assert result['success']
        assert len(result['data']) == 1
        assert '1 pedido(s)' in result['message']
    
    def test_get_my_orders_filtrar_status(self, controller, pedido_mock):
        """Deve filtrar pedidos por status."""
        pedidos = [pedido_mock]
        
        with patch.object(controller.order_service, 'listar_pedidos_usuario', return_value=pedidos):
            result = controller.get_my_orders(status='PENDENTE', limit=5)
        
        assert result['success']
        assert len(result['data']) == 1
    
    def test_get_my_orders_vazio(self, controller):
        """Deve retornar lista vazia."""
        with patch.object(controller.order_service, 'listar_pedidos_usuario', return_value=[]):
            result = controller.get_my_orders()
        
        assert result['success']
        assert len(result['data']) == 0
    
    def test_get_my_orders_exception(self, controller):
        """Deve tratar exceção."""
        with patch.object(controller.order_service, 'listar_pedidos_usuario',
                         side_effect=Exception("Error")):
            result = controller.get_my_orders()
        
        assert not result['success']


class TestOrderControllerGetOrderDetails:
    """Testes de detalhes de pedido."""
    
    def test_get_order_details_sem_usuario(self, mock_main_window):
        """Deve falhar sem usuário logado."""
        controller = OrderController(mock_main_window)
        result = controller.get_order_details(1)
        
        assert not result['success']
    
    def test_get_order_details_sucesso(self, controller, pedido_mock):
        """Deve obter detalhes do pedido."""
        with patch.object(controller.order_service, 'buscar_por_id', return_value=pedido_mock):
            result = controller.get_order_details(1)
        
        assert result['success']
        assert result['data'] == pedido_mock
    
    def test_get_order_details_nao_encontrado(self, controller):
        """Deve falhar quando pedido não existe."""
        with patch.object(controller.order_service, 'buscar_por_id', return_value=None):
            result = controller.get_order_details(999)
        
        assert not result['success']
        assert 'não encontrado' in result['message']
    
    def test_get_order_details_acesso_negado(self, controller, pedido_mock):
        """Deve negar acesso a pedido de outro usuário."""
        pedido_mock['usuario_id'] = 2  # Outro usuário
        
        with patch.object(controller.order_service, 'buscar_por_id', return_value=pedido_mock):
            result = controller.get_order_details(1)
        
        assert not result['success']
        assert 'Acesso negado' in result['message']


class TestOrderControllerCancelOrder:
    """Testes de cancelar pedido."""
    
    def test_cancel_order_sem_usuario(self, mock_main_window):
        """Deve falhar sem usuário logado."""
        controller = OrderController(mock_main_window)
        result = controller.cancel_order(1)
        
        assert not result['success']
    
    def test_cancel_order_sucesso(self, controller, pedido_mock):
        """Deve cancelar pedido com sucesso."""
        with patch.object(controller.order_service, 'buscar_por_id', return_value=pedido_mock):
            with patch.object(controller.order_service, 'cancelar_pedido'):
                result = controller.cancel_order(1)
        
        assert result['success']
        assert 'cancelado' in result['message']
    
    def test_cancel_order_nao_pode_ser_cancelado(self, controller, pedido_mock):
        """Deve falhar quando pedido não pode ser cancelado."""
        with patch.object(controller.order_service, 'buscar_por_id', return_value=pedido_mock):
            with patch.object(controller.order_service, 'cancelar_pedido',
                             side_effect=Exception("Pedido não pode ser cancelado")):
                result = controller.cancel_order(1)
        
        assert not result['success']
        assert 'já foi enviado' in result['message']
    
    def test_cancel_order_prazo_expirado(self, controller, pedido_mock):
        """Deve falhar quando prazo expirou."""
        with patch.object(controller.order_service, 'buscar_por_id', return_value=pedido_mock):
            with patch.object(controller.order_service, 'cancelar_pedido',
                             side_effect=Exception("Prazo expirado")):
                result = controller.cancel_order(1)
        
        assert not result['success']
        assert 'expirou' in result['message']


class TestOrderControllerNavigation:
    """Testes de navegação."""
    
    def test_view_order_sucesso(self, controller, mock_main_window, pedido_mock):
        """Deve navegar para detalhes do pedido."""
        with patch.object(controller.order_service, 'buscar_por_id', return_value=pedido_mock):
            result = controller.view_order(1)
        
        assert result['success']
        mock_main_window.show_view.assert_called_once_with('OrderDetailView', pedido_mock)
    
    def test_view_order_pedido_nao_existe(self, controller, mock_main_window):
        """Não deve navegar quando pedido não existe."""
        with patch.object(controller.order_service, 'buscar_por_id', return_value=None):
            result = controller.view_order(999)
        
        assert not result['success']
        mock_main_window.show_view.assert_not_called()
    
    def test_view_my_orders(self, controller, mock_main_window, pedido_mock):
        """Deve navegar para lista de pedidos."""
        with patch.object(controller.order_service, 'listar_pedidos_usuario', return_value=[pedido_mock]):
            result = controller.view_my_orders()
        
        assert result['success']
        mock_main_window.show_view.assert_called_once_with('MyOrdersView', [pedido_mock])
