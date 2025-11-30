"""
CheckoutController - Controlador de Checkout
===========================================
Gerencia o processo de finalização de compra e cadastro de endereços.
"""
from typing import Dict, Any
from src.controllers.base_controller import BaseController
from src.services.checkout_service import CheckoutService
from src.repositories.cart_repository import CarrinhoRepository
from src.repositories.order_repository import PedidoRepository
from src.repositories.product_repository import ProductRepository
from src.repositories.address_repository import EnderecoRepository
from src.repositories.user_repository import UsuarioRepository 
from src.services.email_service import EmailService
from src.integration.payment.credit_card_gateway import CreditCardGateway
from src.integration.payment.pix_gateway import PixGateway
from src.integration.shipping.correios_calculator import CorreiosCalculator


class CheckoutController(BaseController):
    """
    Controller para operações de checkout e endereço.
    """
    
    def __init__(self, main_window):
        super().__init__(main_window)
        self.carrinho_repo = CarrinhoRepository()
        self.pedido_repo = PedidoRepository()
        self.product_repo = ProductRepository()
        self.address_repo = EnderecoRepository()
        self.user_repo = UsuarioRepository() 
        self.email_service = EmailService()
        self.current_usuario_id = None
        self.frete_calculator = CorreiosCalculator()
    
    def set_current_user(self, usuario_id: int) -> None:
        self.current_usuario_id = usuario_id
    
    def get_shipping_addresses(self) -> Dict[str, Any]:
        """Obtém endereços de entrega do cliente."""
        if not self.current_usuario_id:
            return self._error_response('Usuário não autenticado')
        
        try:
            enderecos = self.address_repo.listar_por_usuario(self.current_usuario_id)
            if not enderecos:
                return self._success_response('Nenhum endereço cadastrado', [])
            return self._success_response('Endereços encontrados', enderecos)
        except Exception as e:
            return self._error_response('Erro ao buscar endereços', e)

    def add_address(self, dados_endereco: Dict[str, Any]) -> Dict[str, Any]:
        """Cadastra um novo endereço para o usuário atual."""
        if not self.current_usuario_id:
            return self._error_response('Usuário não autenticado')

        campos_obrigatorios = ['logradouro', 'numero', 'bairro', 'cidade', 'estado', 'cep']
        for campo in campos_obrigatorios:
            if not dados_endereco.get(campo):
                return self._error_response(f"O campo '{campo}' é obrigatório.")

        try:
            novo_endereco = {
                'usuario_id': self.current_usuario_id,
                'logradouro': dados_endereco['logradouro'],
                'numero': dados_endereco['numero'],
                'complemento': dados_endereco.get('complemento', ''),
                'bairro': dados_endereco['bairro'],
                'cidade': dados_endereco['cidade'],
                'estado': dados_endereco['estado'],
                'cep': dados_endereco['cep'],
                'principal': 1
            }
            
            self.address_repo.salvar(novo_endereco)
            return self._success_response("Endereço cadastrado com sucesso!")
            
        except Exception as e:
            return self._error_response("Erro ao salvar endereço", e)
    
    def process_order(
        self,
        endereco_id: int,
        metodo_pagamento: str,
        dados_pagamento: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Processa o pedido injetando as estratégias corretas."""
        if not self.current_usuario_id:
            return self._error_response('Usuário não autenticado')
        
        if not endereco_id:
            return self._error_response("Selecione um endereço de entrega.")
        if metodo_pagamento not in ['cartao', 'pix']:
            return self._error_response('Método de pagamento inválido')
        
        try:
            carrinho = self.carrinho_repo.buscar_por_usuario(self.current_usuario_id)
            if not carrinho:
                return self._error_response('Carrinho não encontrado')

            itens = carrinho.get('itens')
            if not itens:
                itens = self.carrinho_repo.listar_itens(carrinho['id'])
                if not itens:
                    return self._error_response('Carrinho vazio')
                carrinho['itens'] = itens
            
            if metodo_pagamento == 'cartao':
                gateway = CreditCardGateway()
            else:
                gateway = PixGateway()
            
            checkout_service = CheckoutService(
                carrinho_repo=self.carrinho_repo,
                pedido_repo=self.pedido_repo,
                produto_repo=self.product_repo,
                user_repo=self.user_repo,
                email_service=self.email_service,
                pagamento_gateway=gateway,
                frete_calculator=self.frete_calculator
            )
            
            endereco_obj = self.address_repo.buscar_por_id(endereco_id)
            
            pedido = checkout_service.processar_compra(
                carrinho_id=carrinho['id'],
                dados_pagamento=dados_pagamento,
                endereco_entrega=endereco_obj,
                tipo_pagamento_str=metodo_pagamento 
            )
            
            self.navigate_to('MyOrdersView', {'usuario': self.main_window.current_view.usuario})
            
            return self._success_response('Pedido realizado com sucesso!', pedido)
        
        except ValueError as e:
            return self._error_response(str(e))
        except Exception as e:
            msg = str(e).lower()
            if 'estoque' in msg:
                return self._error_response('Produto sem estoque suficiente.')
            elif 'pagamento' in msg or 'recusado' in msg:
                return self._error_response('Pagamento recusado pela operadora.')
            else:
                print(f"Erro detalhado Checkout: {e}")
                return self._error_response('Erro ao processar pedido', e)