from typing import Dict, Any
from src.models.enums import StatusPedido, StatusPagamento
from src.integration.payment.payment_gateway import PaymentGateway
from src.repositories.cart_repository import CarrinhoRepository
from src.repositories.order_repository import PedidoRepository
from src.repositories.product_repository import ProductRepository
from src.models.sales.order_model import Pedido
from src.models.sales.cart_item_model import ItemPedido
from src.services.email_service import EmailService

class EstoqueInsuficienteError(Exception): pass
class PagamentoRecusadoError(Exception): pass

class CheckoutService:
    def __init__(self, 
                 carrinho_repo: CarrinhoRepository,
                 pedido_repo: PedidoRepository,
                 produto_repo: ProductRepository,
                 email_service: EmailService,
                 pagamento_gateway: PaymentGateway):
        self.carrinho_repo = carrinho_repo
        self.pedido_repo = pedido_repo
        self.produto_repo = produto_repo
        self.email_service = email_service
        self.pagamento_gateway = pagamento_gateway

    def processar_compra(self, carrinho_id: int, dados_pagamento: Dict[str, Any], endereco_id: int) -> Pedido:
        # BUSCAR DADOS DO CARRINHO
        # O repositório retorna um Dict com dados do carrinho, mas NÃO os itens automaticamente
        carrinho_dados = self.carrinho_repo.buscar_por_id(carrinho_id)
        if not carrinho_dados:
            raise ValueError("Carrinho não encontrado.")
            
        # Busca os itens separadamente
        itens = self.carrinho_repo.listar_itens(carrinho_id)
        if not itens:
            raise ValueError("O carrinho está vazio.")
        
        # Calcula total usando o repositório
        valor_total = self.carrinho_repo.calcular_total(carrinho_id)
        
        # 2. INICIAR TRANSAÇÃO
        conexao = self.pedido_repo.iniciar_transacao()
        
        try:
            itens_pedido = []
            
            # 3. VALIDAÇÃO E BAIXA DE ESTOQUE
            for item in itens:
                prod_id = item['produto_id']
                qtd_solicitada = item['quantidade']
                
                # Busca produto na transação (retorna Dict)
                produto = self.produto_repo.buscar_por_id_para_bloqueio(prod_id, conexao)
                
                if produto['estoque'] < qtd_solicitada:
                    raise EstoqueInsuficienteError(f"Estoque insuficiente para {produto['nome']}.")
                
                # Abate estoque
                novo_estoque = produto['estoque'] - qtd_solicitada
                self.produto_repo.atualizar_estoque(prod_id, novo_estoque, conexao)

                # Cria objeto ItemPedido para o registro
                item_pedido = ItemPedido(
                    produto_id=prod_id,
                    quantidade=qtd_solicitada,
                    preco_unitario=item['preco_unitario']
                )
                itens_pedido.append(item_pedido)

            # 4. PAGAMENTO
            pagamento_status = self.pagamento_gateway.processar_pagamento(
                valor_total, 
                dados_pagamento
            )

            if pagamento_status == StatusPagamento.REJEITADO:
                raise PagamentoRecusadoError("Pagamento recusado.")
            
            # 5. CRIAR PEDIDO
            status_final = StatusPedido.PROCESSANDO if pagamento_status == StatusPagamento.APROVADO else StatusPedido.PAGAMENTO_PENDENTE

            # Recupera cliente_id do dicionário do carrinho
            cliente_id = carrinho_dados['usuario_id']

            novo_pedido = Pedido(
                cliente_id=cliente_id,
                endereco_entrega_id=endereco_id,
                valor_total=valor_total,
                status=status_final,
                itens=itens_pedido
            )
            
            self.pedido_repo.salvar_pedido_e_itens(novo_pedido, conexao)
            self.pedido_repo.commit_transacao(conexao)
            
            # 6. LIMPEZA E NOTIFICAÇÃO
            self.carrinho_repo.limpar(carrinho_id)
            self.email_service.enviar_confirmacao(novo_pedido)

            return novo_pedido

        except Exception as e:
            self.pedido_repo.rollback_transacao(conexao)
            print(f"Erro no checkout (Rollback): {e}")
            raise e