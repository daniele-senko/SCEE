"""
CartController - Controlador de Carrinho
========================================

Gerencia operações do carrinho de compras.
"""
from typing import Dict, Any
from src.controllers.base_controller import BaseController
from src.services.cart_service import CarrinhoService
from src.repositories.cart_repository import CarrinhoRepository
from src.repositories.product_repository import ProductRepository


class CartController(BaseController):
    """
    Controller para operações de carrinho.
    
    Métodos:
    - add_to_cart(): Adiciona produto ao carrinho
    - remove_from_cart(): Remove item do carrinho
    - update_quantity(): Atualiza quantidade de item
    - clear_cart(): Limpa carrinho
    - get_cart(): Obtém carrinho atual
    - view_cart(): Navega para tela do carrinho
    """
    
    def __init__(self, main_window):
        super().__init__(main_window)
        self.cart_service = CarrinhoService(
            CarrinhoRepository(),
            ProductRepository()
        )
        self.current_usuario_id = None
    
    def set_current_user(self, usuario_id: int) -> None:
        """
        Define o usuário atual.
        
        Args:
            usuario_id: ID do usuário logado
        """
        self.current_usuario_id = usuario_id
    
    def add_to_cart(
        self,
        produto_id: int,
        quantidade: int = 1
    ) -> Dict[str, Any]:
        """
        Adiciona produto ao carrinho.
        
        Args:
            produto_id: ID do produto
            quantidade: Quantidade a adicionar
            
        Returns:
            Dicionário com success, message e data (item)
        """
        if not self.current_usuario_id:
            return self._error_response('Usuário não autenticado')
        
        # Validar quantidade
        if quantidade <= 0:
            return self._error_response('Quantidade deve ser maior que zero')
        
        try:
            item = self.cart_service.adicionar_item(
                self.current_usuario_id,
                produto_id,
                quantidade
            )
            
            return self._success_response(
                'Produto adicionado ao carrinho',
                item
            )
        
        except Exception as e:
            error_msg = str(e)
            
            # Customizar mensagens de erro comuns
            if 'estoque insuficiente' in error_msg.lower():
                return self._error_response('Produto sem estoque disponível')
            elif 'produto não encontrado' in error_msg.lower():
                return self._error_response('Produto não disponível')
            elif 'limite' in error_msg.lower():
                return self._error_response(error_msg)
            else:
                return self._error_response(
                    'Erro ao adicionar produto ao carrinho',
                    e
                )
    
    def remove_from_cart(self, item_id: int) -> Dict[str, Any]:
        """
        Remove item do carrinho.
        
        Args:
            item_id: ID do item do carrinho
            
        Returns:
            Dicionário com success e message
        """
        if not self.current_usuario_id:
            return self._error_response('Usuário não autenticado')
        
        try:
            self.cart_service.remover_item(item_id)
            
            return self._success_response('Produto removido do carrinho')
        
        except Exception as e:
            return self._error_response(
                'Erro ao remover produto',
                e
            )
    
    def update_quantity(
        self,
        item_id: int,
        nova_quantidade: int
    ) -> Dict[str, Any]:
        """
        Atualiza quantidade de um item.
        
        Args:
            item_id: ID do item
            nova_quantidade: Nova quantidade
            
        Returns:
            Dicionário com success e message
        """
        if not self.current_usuario_id:
            return self._error_response('Usuário não autenticado')
        
        if nova_quantidade < 0:
            return self._error_response('Quantidade inválida')
        
        if nova_quantidade == 0:
            return self.remove_from_cart(item_id)
        
        try:
            self.cart_service.atualizar_quantidade(
                self.current_usuario_id,
                item_id,
                nova_quantidade
            )
            
            return self._success_response('Quantidade atualizada')
        
        except Exception as e:
            error_msg = str(e)
            
            if 'estoque' in error_msg.lower():
                return self._error_response('Estoque insuficiente')
            else:
                return self._error_response(
                    'Erro ao atualizar quantidade',
                    e
                )
    
    def clear_cart(self) -> Dict[str, Any]:
        """
        Limpa o carrinho.
        
        Returns:
            Dicionário com success e message
        """
        if not self.current_usuario_id:
            return self._error_response('Usuário não autenticado')
        
        try:
            carrinho = self.cart_service.obter_ou_criar_carrinho(
                self.current_usuario_id
            )
            
            self.cart_service.limpar_carrinho(carrinho['id'])
            
            return self._success_response('Carrinho limpo')
        
        except Exception as e:
            return self._error_response(
                'Erro ao limpar carrinho',
                e
            )
    
    def get_cart(self) -> Dict[str, Any]:
        """
        Obtém o carrinho atual com itens.
        
        Returns:
            Dicionário com success, message e data (carrinho com itens)
        """
        if not self.current_usuario_id:
            return self._error_response('Usuário não autenticado')
        
        try:
            carrinho = self.cart_service.obter_ou_criar_carrinho(
                self.current_usuario_id
            )
            
            print(f"DEBUG get_cart: Carrinho obtido = {carrinho}")
            
            itens = self.cart_service.listar_itens(carrinho['id'])
            
            print(f"DEBUG get_cart: Itens retornados = {itens}")
            print(f"DEBUG get_cart: Quantidade de itens = {len(itens)}")
            
            total = self.cart_service.calcular_total(carrinho['id'])
            
            # Estrutura corrigida para compatibilidade com a view
            cart_data = {
                'id': carrinho['id'],
                'usuario_id': carrinho['usuario_id'],
                'itens': itens,
                'total': total,
                'quantidade_itens': len(itens)
            }
            
            print(f"DEBUG get_cart: cart_data final = {cart_data}")
            
            return self._success_response(
                f'{len(itens)} item(ns) no carrinho',
                cart_data
            )
        
        except Exception as e:
            return self._error_response(
                'Erro ao obter carrinho',
                e
            )
    
    def view_cart(self) -> Dict[str, Any]:
        """
        Navega para a tela do carrinho.
        
        Returns:
            Dicionário com success e message
        """
        result = self.get_cart()
        
        if result['success']:
            self.navigate_to('CartView', result['data'])
        
        return result
    
    def proceed_to_checkout(self) -> Dict[str, Any]:
        """
        Inicia processo de checkout.
        
        Returns:
            Dicionário com success e message
        """
        # Validar se há itens no carrinho
        result = self.get_cart()
        
        if not result['success']:
            return result
        
        cart_data = result['data']
        
        if not cart_data['itens']:
            return self._error_response('Carrinho vazio')
        
        # Navegar para checkout
        self.navigate_to('CheckoutView', cart_data)
        
        return self._success_response('Iniciando checkout')
