"""
OrderController - Controlador de Pedidos
========================================

Gerencia criação e consulta de pedidos.
"""
from typing import Dict, Any, List
from src.controllers.base_controller import BaseController
from src.services.order_service import PedidoService
from src.repositories.order_repository import PedidoRepository
from src.repositories.product_repository import ProductRepository
from src.repositories.user_repository import UsuarioRepository


class OrderController(BaseController):
    """
    Controller para operações de pedidos.
    
    Métodos:
    - create_order(): Cria novo pedido
    - get_my_orders(): Lista pedidos do usuário
    - get_order_details(): Detalhes de um pedido
    - cancel_order(): Cancela pedido
    - view_order(): Navega para detalhes do pedido
    """
    
    def __init__(self, main_window):
        super().__init__(main_window)
        self.order_service = PedidoService(
            PedidoRepository(),
            ProductRepository(),
            UsuarioRepository()
        )
        self.current_usuario_id = None
    
    def set_current_user(self, usuario_id: int) -> None:
        """
        Define o usuário atual.
        
        Args:
            usuario_id: ID do usuário logado
        """
        self.current_usuario_id = usuario_id
    
    def create_order(
        self,
        endereco_id: int,
        itens: List[Dict[str, Any]],
        tipo_pagamento: str,
        frete: float = 0.0,
        observacoes: str = None
    ) -> Dict[str, Any]:
        """
        Cria novo pedido.
        
        Args:
            endereco_id: ID do endereço de entrega
            itens: Lista de itens [{produto_id, quantidade, preco_unitario}]
            tipo_pagamento: Tipo de pagamento (PIX, CARTAO, BOLETO)
            frete: Valor do frete
            observacoes: Observações opcionais
            
        Returns:
            Dicionário com success, message e data (pedido)
        """
        if not self.current_usuario_id:
            return self._error_response('Usuário não autenticado')
        
        # Validações
        if not itens:
            return self._error_response('Pedido deve ter pelo menos um item')
        
        if tipo_pagamento not in ['PIX', 'CARTAO', 'BOLETO']:
            return self._error_response('Tipo de pagamento inválido')
        
        try:
            pedido = self.order_service.criar_pedido(
                usuario_id=self.current_usuario_id,
                endereco_id=endereco_id,
                itens=itens,
                tipo_pagamento=tipo_pagamento,
                frete=frete,
                observacoes=observacoes
            )
            
            return self._success_response(
                f'Pedido #{pedido["id"]} criado com sucesso!',
                pedido
            )
        
        except Exception as e:
            error_msg = str(e)
            
            if 'estoque' in error_msg.lower():
                return self._error_response('Produto sem estoque disponível')
            elif 'endereço' in error_msg.lower():
                return self._error_response('Endereço inválido')
            else:
                return self._error_response(
                    'Erro ao criar pedido',
                    e
                )
    
    def get_my_orders(
        self,
        status: str = None,
        limit: int = 10
    ) -> Dict[str, Any]:
        """
        Lista pedidos do usuário.
        
        Args:
            status: Filtrar por status (opcional)
            limit: Limite de resultados
            
        Returns:
            Dicionário com success, message e data (lista de pedidos)
        """
        if not self.current_usuario_id:
            return self._error_response('Usuário não autenticado')
        
        try:
            pedidos = self.order_service.listar_pedidos_usuario(
                self.current_usuario_id,
                status=status,
                limit=limit
            )
            
            return self._success_response(
                f'{len(pedidos)} pedido(s) encontrado(s)',
                pedidos
            )
        
        except Exception as e:
            return self._error_response(
                'Erro ao listar pedidos',
                e
            )
    
    def get_order_details(self, pedido_id: int) -> Dict[str, Any]:
        """
        Obtém detalhes completos de um pedido.
        
        Args:
            pedido_id: ID do pedido
            
        Returns:
            Dicionário com success, message e data (pedido completo)
        """
        if not self.current_usuario_id:
            return self._error_response('Usuário não autenticado')
        
        try:
            pedido = self.order_service.obter_detalhes_pedido(pedido_id)
            
            if not pedido:
                return self._error_response('Pedido não encontrado')
            
            # Verificar se o pedido pertence ao usuário
            if pedido['usuario_id'] != self.current_usuario_id:
                return self._error_response('Acesso negado')
            
            return self._success_response(
                'Pedido encontrado',
                pedido
            )
        
        except Exception as e:
            return self._error_response(
                'Erro ao buscar pedido',
                e
            )
    
    def cancel_order(self, pedido_id: int) -> Dict[str, Any]:
        """
        Cancela um pedido.
        
        Args:
            pedido_id: ID do pedido
            
        Returns:
            Dicionário com success e message
        """
        if not self.current_usuario_id:
            return self._error_response('Usuário não autenticado')
        
        try:
            # Verificar se pedido pertence ao usuário
            result = self.get_order_details(pedido_id)
            if not result['success']:
                return result
            
            # Cancelar pedido
            self.order_service.cancelar_pedido(pedido_id)
            
            return self._success_response(
                f'Pedido #{pedido_id} cancelado'
            )
        
        except Exception as e:
            error_msg = str(e)
            
            if 'não pode ser cancelado' in error_msg.lower():
                return self._error_response(
                    'Pedido não pode ser cancelado (já foi enviado)'
                )
            elif 'prazo' in error_msg.lower():
                return self._error_response(
                    'Prazo para cancelamento expirou'
                )
            else:
                return self._error_response(
                    'Erro ao cancelar pedido',
                    e
                )
    
    def view_order(self, pedido_id: int) -> Dict[str, Any]:
        """
        Navega para a tela de detalhes do pedido.
        
        Args:
            pedido_id: ID do pedido
            
        Returns:
            Dicionário com success e message
        """
        result = self.get_order_details(pedido_id)
        
        if result['success']:
            self.navigate_to('OrderDetailView', result['data'])
        
        return result
    
    def view_my_orders(self) -> Dict[str, Any]:
        """
        Navega para a tela de meus pedidos.
        
        Returns:
            Dicionário com success e message
        """
        result = self.get_my_orders()
        
        if result['success']:
            self.navigate_to('MyOrdersView', result['data'])
        
        return result
