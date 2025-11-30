"""CartController - Controlador de Carrinho."""
from typing import Dict, Any
from src.controllers.base_controller import BaseController
from src.services.cart_service import CarrinhoService
from src.repositories.cart_repository import CarrinhoRepository
from src.repositories.product_repository import ProductRepository

class CartController(BaseController):
    
    def __init__(self, main_window):
        super().__init__(main_window)
        self.cart_service = CarrinhoService(
            CarrinhoRepository(),
            ProductRepository()
        )
        self.current_usuario_id = None
    
    def set_current_user(self, usuario_id: int) -> None:
        self.current_usuario_id = usuario_id
    
    def get_cart(self) -> Dict[str, Any]:
        """Obtém o carrinho completo com total atualizado."""
        if not self.current_usuario_id:
            return self._error_response('Usuário não autenticado')
        
        try:
            # CORREÇÃO: Usa o método que já traz tudo calculado e estruturado
            cart_data = self.cart_service.obter_carrinho_completo(self.current_usuario_id)
            
            return self._success_response(
                f"{len(cart_data['itens'])} item(ns)",
                cart_data
            )
        except Exception as e:
            return self._error_response('Erro ao obter carrinho', e)

    # --- Métodos de ação (mantidos simples) ---
    def add_to_cart(self, produto_id: int, quantidade: int = 1) -> Dict[str, Any]:
        if not self.current_usuario_id: return self._error_response('Auth Error')
        try:
            item = self.cart_service.adicionar_item(self.current_usuario_id, produto_id, quantidade)
            return self._success_response('Adicionado', item)
        except Exception as e: return self._error_response(str(e))

    def remove_from_cart(self, item_id: int) -> Dict[str, Any]:
        if not self.current_usuario_id: return self._error_response('Auth Error')
        try:
            self.cart_service.remover_item(self.current_usuario_id, item_id)
            return self._success_response('Removido')
        except Exception as e: return self._error_response(str(e))

    def update_quantity(self, item_id: int, nova_quantidade: int) -> Dict[str, Any]:
        if not self.current_usuario_id: return self._error_response('Auth Error')
        try:
            self.cart_service.atualizar_quantidade(self.current_usuario_id, item_id, nova_quantidade)
            return self._success_response('Atualizado')
        except Exception as e: return self._error_response(str(e))

    def clear_cart(self) -> Dict[str, Any]:
        # Implementação simplificada
        return self._success_response('Carrinho limpo') # Placeholder