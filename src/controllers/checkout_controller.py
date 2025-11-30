"""
CheckoutController - Controlador de Checkout
===========================================

Gerencia o processo de finalização de compra.
"""
from typing import Dict, Any
from src.controllers.base_controller import BaseController
from src.services.checkout_service import CheckoutService
from src.repositories.cart_repository import CarrinhoRepository
from src.repositories.order_repository import PedidoRepository
from src.repositories.product_repository import ProductRepository
from src.repositories.address_repository import EnderecoRepository
from src.services.email_service import EmailService
from src.integration.pagamento_gateway import PagamentoCartao, PagamentoPix


class CheckoutController(BaseController):
    """
    Controller para operações de checkout.
    
    Métodos:
    - get_shipping_addresses(): Lista endereços do cliente
    - process_order(): Processa pedido com pagamento
    """
    
    def __init__(self, main_window):
        super().__init__(main_window)
        self.carrinho_repo = CarrinhoRepository()
        self.pedido_repo = PedidoRepository()
        self.product_repo = ProductRepository()
        self.address_repo = EnderecoRepository()
        self.email_service = EmailService()
        self.current_usuario_id = None
    
    def set_current_user(self, usuario_id: int) -> None:
        """
        Define o usuário atual.
        
        Args:
            usuario_id: ID do usuário logado
        """
        self.current_usuario_id = usuario_id
    
    def get_shipping_addresses(self) -> Dict[str, Any]:
        """
        Obtém endereços de entrega do cliente.
        
        Returns:
            Dicionário com success, message e data (lista de endereços)
        """
        if not self.current_usuario_id:
            return self._error_response('Usuário não autenticado')
        
        try:
            enderecos = self.address_repo.buscar_por_cliente(self.current_usuario_id)
            
            if not enderecos:
                return self._success_response(
                    'Nenhum endereço cadastrado',
                    []
                )
            
            return self._success_response(
                'Endereços encontrados',
                enderecos
            )
        
        except Exception as e:
            return self._error_response(
                'Erro ao buscar endereços',
                e
            )
    
    def process_order(
        self,
        endereco_id: int,
        metodo_pagamento: str,
        dados_pagamento: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Processa o pedido com pagamento.
        
        Args:
            endereco_id: ID do endereço de entrega
            metodo_pagamento: 'cartao' ou 'pix'
            dados_pagamento: Dados específicos do método de pagamento
            
        Returns:
            Dicionário com success, message e data (pedido)
        """
        if not self.current_usuario_id:
            return self._error_response('Usuário não autenticado')
        
        # Validações
        error = self._validate_not_empty(endereco_id, "Endereço")
        if error:
            return self._error_response(error)
        
        error = self._validate_not_empty(metodo_pagamento, "Método de pagamento")
        if error:
            return self._error_response(error)
        
        if metodo_pagamento not in ['cartao', 'pix']:
            return self._error_response('Método de pagamento inválido')
        
        try:
            # Busca o carrinho do usuário
            carrinho = self.carrinho_repo.buscar_por_cliente(self.current_usuario_id)
            
            if not carrinho:
                return self._error_response('Carrinho não encontrado')
            
            if not carrinho.get('itens'):
                return self._error_response('Carrinho está vazio')
            
            # Seleciona o gateway de pagamento apropriado
            if metodo_pagamento == 'cartao':
                gateway = PagamentoCartao()
            else:  # pix
                gateway = PagamentoPix()
            
            # Cria o serviço de checkout com as dependências
            checkout_service = CheckoutService(
                carrinho_repo=self.carrinho_repo,
                pedido_repo=self.pedido_repo,
                produto_repo=self.product_repo,
                email_service=self.email_service,
                pagamento_gateway=gateway
            )
            
            # Processa a compra
            pedido = checkout_service.processar_compra(
                carrinho_id=carrinho['id'],
                dados_pagamento=dados_pagamento,
                endereco_id=endereco_id
            )
            
            # Navega para tela de pedidos após sucesso
            self.navigate_to('MyOrdersView', self.main_window.current_view.usuario)
            
            return self._success_response(
                'Pedido realizado com sucesso!',
                pedido
            )
        
        except ValueError as e:
            return self._error_response(str(e))
        
        except Exception as e:
            error_msg = str(e)
            
            # Customizar mensagens de erro
            if 'estoque' in error_msg.lower():
                return self._error_response('Produto sem estoque disponível')
            elif 'pagamento' in error_msg.lower() or 'rejeit' in error_msg.lower():
                return self._error_response('Pagamento recusado. Verifique os dados.')
            else:
                return self._error_response(
                    'Erro ao processar pedido',
                    e
                )
