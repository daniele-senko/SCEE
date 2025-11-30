"""
OrderController - Controlador de Pedidos
========================================
Gerencia a visualização de pedidos do cliente.
"""
from typing import Dict, Any
from src.controllers.base_controller import BaseController
from src.repositories.order_repository import PedidoRepository
from src.repositories.product_repository import ProductRepository
from src.repositories.user_repository import UsuarioRepository
from src.services.order_service import PedidoService

class OrderController(BaseController):
    """
    Controlador para operações relacionadas a pedidos.
    """
    
    def __init__(self, main_window):
        super().__init__(main_window)
        self.order_repo = PedidoRepository()
        self.product_repo = ProductRepository()
        self.user_repo = UsuarioRepository()
        
        # Instancia o serviço
        self.order_service = PedidoService(
            self.order_repo,
            self.product_repo,
            self.user_repo
        )
        self.current_usuario_id = None
    
    def set_current_user(self, usuario_id: int) -> None:
        self.current_usuario_id = usuario_id

    # --- MÉTODO QUE FALTAVA ---
    def list_my_orders(self) -> Dict[str, Any]:
        """
        Lista os pedidos do usuário logado.
        Usado pela MyOrdersView.
        """
        if not self.current_usuario_id:
            return self._error_response('Usuário não autenticado')
            
        try:
            # Chama o repositório diretamente para leitura (mais eficiente)
            # ou o service se tiver regras de negócio (ex: formatação)
            pedidos = self.order_repo.listar_por_usuario(self.current_usuario_id)
            
            # Formata ou enriquece os dados se necessário
            # Ex: Garantir que 'total' seja float
            for p in pedidos:
                p['total'] = float(p['total'])
                
                # Se não tiver a lista de itens carregada, busca agora
                # (O listar_por_usuario do repo simples pode não trazer itens)
                if 'itens' not in p:
                    p['itens'] = self.order_repo.listar_itens(p['id'])

            return self._success_response(
                f'{len(pedidos)} pedidos encontrados', 
                pedidos
            )
            
        except Exception as e:
            return self._error_response('Erro ao listar pedidos', e)

    def get_order_details(self, pedido_id: int) -> Dict[str, Any]:
        """Busca detalhes de um pedido específico."""
        try:
            pedido = self.order_service.buscar_por_id(pedido_id, completo=True)
            if not pedido:
                return self._error_response('Pedido não encontrado')
            return self._success_response('Detalhes recuperados', pedido)
        except Exception as e:
            return self._error_response('Erro ao buscar detalhes', e)