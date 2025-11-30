from typing import Dict, Any
from src.models.enums import StatusPedido, StatusPagamento
from src.models.sales.order_model import Pedido
from src.models.sales.cart_item_model import ItemPedido

from src.integration.payment.payment_gateway import PaymentGateway
from src.integration.shipping.shipping_calculator import ShippingCalculator

from src.repositories.cart_repository import CarrinhoRepository
from src.repositories.order_repository import PedidoRepository
from src.repositories.product_repository import ProdutoRepository
from src.services.email_service import EmailService

class EstoqueInsuficienteError(Exception): pass
class PagamentoRecusadoError(Exception): pass

class CheckoutService:
    def __init__(self, 
                 carrinho_repo: CarrinhoRepository,
                 pedido_repo: PedidoRepository,
                 produto_repo: ProdutoRepository,
                 email_service: EmailService,
                 pagamento_gateway: PaymentGateway,      # Injeção 1
                 frete_calculator: ShippingCalculator):  # Injeção 2
        
        self.carrinho_repo = carrinho_repo
        self.pedido_repo = pedido_repo
        self.produto_repo = produto_repo
        self.email_service = email_service
        self.pagamento_gateway = pagamento_gateway
        self.frete_calculator = frete_calculator

    def processar_compra(self, carrinho_id: int, dados_pagamento: Dict[str, Any], endereco_entrega: Dict[str, Any]) -> Pedido:
        # Busca Carrinho
        carrinho = self.carrinho_repo.buscar_por_id(carrinho_id)
        if not carrinho or not carrinho.itens:
            raise ValueError("Carrinho vazio.")

        # Calcula Frete 
        # Vamos assumir peso 1.0kg por item para simplificar a simulação
        peso_total = sum([item.quantidade * 1.0 for item in carrinho.itens])
        cep = endereco_entrega.get('cep', '00000-000')
        valor_frete = self.frete_calculator.calcular(cep, peso_total)

        # Calcula Totais
        subtotal = carrinho.calcular_total()
        valor_total = subtotal + valor_frete

        # Inicia Transação
        conexao = self.pedido_repo.iniciar_transacao()
        
        try:
            itens_pedido = []
            
            # Validação e Baixa de Estoque
            for item_carrinho in carrinho.itens:
                produto = self.produto_repo.buscar_por_id_para_bloqueio(item_carrinho.produto_id, conexao)
                
                if produto.estoque < item_carrinho.quantidade:
                    raise EstoqueInsuficienteError(f"Estoque insuficiente: {produto.nome}")
                
                produto.estoque -= item_carrinho.quantidade
                self.produto_repo.atualizar_estoque(produto, conexao)

                itens_pedido.append(ItemPedido(
                    produto_id=produto.id,
                    quantidade=item_carrinho.quantidade,
                    preco_unitario=produto.preco
                ))

            # Processa Pagamento
            status_pag = self.pagamento_gateway.processar_pagamento(valor_total, dados_pagamento)
            
            if status_pag == StatusPagamento.REJEITADO:
                raise PagamentoRecusadoError("Pagamento não autorizado.")

            # Cria Pedido
            status_pedido = StatusPedido.PROCESSANDO if status_pag == StatusPagamento.APROVADO else StatusPedido.PAGAMENTO_PENDENTE
            
            novo_pedido = Pedido(
                cliente_id=carrinho.cliente_id,
                endereco_entrega_id=endereco_entrega.get('id'),
                valor_total=valor_total,
                status=status_pedido,
                itens=itens_pedido
            )
            # Nota: Você precisará garantir que seu PedidoModel aceite 'frete' se quiser salvar separado
            
            self.pedido_repo.salvar_pedido_e_itens(novo_pedido, conexao)
            self.pedido_repo.commit_transacao(conexao)
            
            self.carrinho_repo.limpar_carrinho(carrinho_id)
            self.email_service.enviar_confirmacao(novo_pedido)
            
            return novo_pedido

        except Exception as e:
            self.pedido_repo.rollback_transacao(conexao)
            raise e