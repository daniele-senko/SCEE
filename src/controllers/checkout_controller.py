"""
CheckoutController - Controlador de Checkout
===========================================
Gerencia o processo de finalização de compra com Polimorfismo.
"""
from typing import Dict, Any
from src.controllers.base_controller import BaseController
from src.services.checkout_service import CheckoutService
from src.repositories.cart_repository import CarrinhoRepository
from src.repositories.order_repository import PedidoRepository
from src.repositories.product_repository import ProductRepository
from src.repositories.address_repository import EnderecoRepository
from src.services.email_service import EmailService
from src.integration.payment.credit_card_gateway import CreditCardGateway
from src.integration.payment.pix_gateway import PixGateway
from src.integration.shipping.correios_calculator import CorreiosCalculator


class CheckoutController(BaseController):
    """
    Controller para operações de checkout.
    Orquestra a injeção de dependências das estratégias de Pagamento e Frete.
    """
    
    def __init__(self, main_window):
        super().__init__(main_window)
        self.carrinho_repo = CarrinhoRepository()
        self.pedido_repo = PedidoRepository()
        self.product_repo = ProductRepository()
        self.address_repo = EnderecoRepository()
        self.email_service = EmailService()
        self.current_usuario_id = None
        
        # Estratégia de Frete Padrão (Poderia vir de configuração)
        self.frete_calculator = CorreiosCalculator()
    
    def set_current_user(self, usuario_id: int) -> None:
        self.current_usuario_id = usuario_id
    
    def get_shipping_addresses(self) -> Dict[str, Any]:
        """Obtém endereços de entrega do cliente."""
        if not self.current_usuario_id:
            return self._error_response('Usuário não autenticado')
        
        try:
            enderecos = self.address_repo.buscar_por_cliente(self.current_usuario_id)
            if not enderecos:
                return self._success_response('Nenhum endereço cadastrado', [])
            return self._success_response('Endereços encontrados', enderecos)
        except Exception as e:
            return self._error_response('Erro ao buscar endereços', e)
    
    def process_order(
        self,
        endereco_id: int,
        metodo_pagamento: str,
        dados_pagamento: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Processa o pedido injetando as estratégias corretas.
        """
        if not self.current_usuario_id:
            return self._error_response('Usuário não autenticado')
        
        # Validações Básicas
        if not endereco_id:
            return self._error_response("Selecione um endereço de entrega.")
        if metodo_pagamento not in ['cartao', 'pix']:
            return self._error_response('Método de pagamento inválido')
        
        try:
            # Busca o carrinho
            carrinho = self.carrinho_repo.buscar_por_cliente(self.current_usuario_id)
            if not carrinho or not carrinho.get('itens'):
                return self._error_response('Carrinho vazio ou não encontrado')
            
            # SELEÇÃO DE ESTRATÉGIA (Factory)
            # Instancia a classe concreta baseada na escolha do usuário
            if metodo_pagamento == 'cartao':
                gateway = CreditCardGateway()
            else:
                gateway = PixGateway()
            
            # INJEÇÃO DE DEPENDÊNCIA (Incluindo Frete e Pagamento)
            checkout_service = CheckoutService(
                carrinho_repo=self.carrinho_repo,
                pedido_repo=self.pedido_repo,
                produto_repo=self.product_repo,
                email_service=self.email_service,
                pagamento_gateway=gateway,          # <--- Polimorfismo Pagamento
                frete_calculator=self.frete_calculator # <--- Polimorfismo Frete
            )
            
            # Busca dados completos do endereço para cálculo de frete
            # (Assumindo que o método buscar_por_id retorna dict com 'cep')
            endereco_obj = self.address_repo.buscar_por_id(endereco_id)
            
            # Processa a compra
            pedido = checkout_service.processar_compra(
                carrinho_id=carrinho['id'],
                dados_pagamento=dados_pagamento,
                endereco_entrega=endereco_obj # Passamos o objeto/dict completo
            )
            
            # Sucesso e Navegação
            self.navigate_to('MyOrdersView', {'usuario': self.main_window.current_view.usuario})
            
            return self._success_response(
                'Pedido realizado com sucesso!',
                pedido
            )
        
        except ValueError as e:
            return self._error_response(str(e))
        except Exception as e:
            # Tratamento de erros de negócio
            msg = str(e).lower()
            if 'estoque' in msg:
                return self._error_response('Produto sem estoque suficiente.')
            elif 'pagamento' in msg or 'recusado' in msg:
                return self._error_response('Pagamento recusado pela operadora.')
            else:
                print(f"Erro detalhado Checkout: {e}") # Log para debug
                return self._error_response('Erro ao processar pedido', e)