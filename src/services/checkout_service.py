from typing import Dict, Any
from src.models.enums import StatusPedido, StatusPagamento
from src.integration.payment.payment_gateway import PaymentGateway
from src.integration.shipping.shipping_calculator import ShippingCalculator
from src.repositories.cart_repository import CarrinhoRepository
from src.repositories.order_repository import PedidoRepository
from src.repositories.product_repository import ProductRepository
from src.repositories.user_repository import UsuarioRepository
from src.models.sales.order_model import Pedido
from src.models.sales.cart_item_model import ItemPedido
from src.models.products.product_model import Produto
from src.models.products.category_model import Categoria
from src.services.email_service import EmailService

class EstoqueInsuficienteError(Exception):
    pass

class PagamentoRecusadoError(Exception):
    pass

class CheckoutService:
    """
    Responsável por orquestrar todo o processo de finalização do pedido.
    Garante a integridade transacional (RNF07.1).
    """

    def __init__(self, 
                 carrinho_repo: CarrinhoRepository,
                 pedido_repo: PedidoRepository,
                 produto_repo: ProductRepository,
                 user_repo: UsuarioRepository,
                 email_service: EmailService,
                 pagamento_gateway: PaymentGateway,
                 frete_calculator: ShippingCalculator):
        
        self.carrinho_repo = carrinho_repo
        self.pedido_repo = pedido_repo
        self.produto_repo = produto_repo
        self.user_repo = user_repo
        self.email_service = email_service
        self.pagamento_gateway = pagamento_gateway
        self.frete_calculator = frete_calculator

    def processar_compra(self, 
                         carrinho_id: int, 
                         dados_pagamento: Dict[str, Any], 
                         endereco_entrega: Dict[str, Any],
                         tipo_pagamento_str: str) -> Pedido:
        
        # 1. BUSCAR DADOS DO CARRINHO
        carrinho_dados = self.carrinho_repo.buscar_por_id(carrinho_id)
        if not carrinho_dados:
            raise ValueError("Carrinho não encontrado.")
            
        itens = self.carrinho_repo.listar_itens(carrinho_id)
        if not itens:
            raise ValueError("O carrinho está vazio.")
        
        # 2. CALCULAR FRETE
        peso_total = sum([item['quantidade'] * 1.0 for item in itens])
        cep_destino = endereco_entrega.get('cep', '00000-000')
        valor_frete = self.frete_calculator.calcular(cep_destino, peso_total)

        # 3. CALCULAR TOTAIS
        subtotal = self.carrinho_repo.calcular_total(carrinho_id)
        valor_total = subtotal + valor_frete
        
        # 4. INICIAR TRANSAÇÃO
        conexao = self.pedido_repo.iniciar_transacao()
        
        try:
            itens_pedido_objs = []
            
            # 5. VALIDAÇÃO E BAIXA DE ESTOQUE
            for item in itens:
                prod_id = item['produto_id']
                qtd_solicitada = item['quantidade']
                
                prod_dict = self.produto_repo.buscar_por_id_para_bloqueio(prod_id, conexao)
                
                if prod_dict['estoque'] < qtd_solicitada:
                    raise EstoqueInsuficienteError(f"Estoque insuficiente para {prod_dict['nome']}.")
                
                novo_estoque = prod_dict['estoque'] - qtd_solicitada
                self.produto_repo.atualizar_estoque(prod_id, novo_estoque, conexao)

                cat_obj = Categoria(
                    nome="Ref",
                    id=prod_dict.get('categoria_id')
                )
                
                produto_obj = Produto(
                    nome=prod_dict['nome'],
                    sku=prod_dict['sku'],
                    preco=prod_dict['preco'],
                    categoria=cat_obj,
                    estoque=novo_estoque,
                    id=prod_dict['id']
                )

                item_pedido = ItemPedido(
                    produto=produto_obj,
                    quantidade=qtd_solicitada,
                    preco_unitario=item['preco_unitario']
                )
                itens_pedido_objs.append(item_pedido)

            # 6. PAGAMENTO
            pagamento_status = self.pagamento_gateway.processar_pagamento(
                valor_total, 
                dados_pagamento
            )

            if pagamento_status == StatusPagamento.REJEITADO:
                raise PagamentoRecusadoError("Pagamento recusado.")
            
            # 7. CRIAR PEDIDO
            status_final = StatusPedido.PROCESSANDO if pagamento_status == StatusPagamento.APROVADO else StatusPedido.PAGAMENTO_PENDENTE

            cliente_id = carrinho_dados['usuario_id']
            endereco_id = endereco_entrega['id']
            
            # Normaliza string para o banco (CARTAO ou PIX)
            tipo_normalizado = "CARTAO" if tipo_pagamento_str == "cartao" else "PIX"

            novo_pedido = Pedido(
                cliente_id=cliente_id,
                endereco_entrega_id=endereco_id,
                tipo_pagamento=tipo_normalizado,
                valor_total=valor_total,
                status=status_final,
                itens=itens_pedido_objs,
                frete=valor_frete
            )
            
            self.pedido_repo.salvar_pedido_e_itens(novo_pedido, conexao)
            self.pedido_repo.commit_transacao(conexao)
            
            # 8. LIMPEZA E NOTIFICAÇÃO
            self.carrinho_repo.limpar(carrinho_id)
            
            usuario = self.user_repo.buscar_por_id(cliente_id)
            if usuario:
                # CORREÇÃO AQUI: usuario.to_dict() para evitar o erro 'not subscriptable'
                self.email_service.enviar_confirmacao_pedido(usuario.to_dict(), novo_pedido.to_dict())

            return novo_pedido

        except Exception as e:
            self.pedido_repo.rollback_transacao(conexao)
            raise e