from typing import Dict, Any
from models.enums import StatusPedido, StatusPagamento
from integration.pagamento_gateway import GatewayPagamentoBase # Interface
from repositories.carrinho_repository import CarrinhoRepository
from repositories.pedido_repository import PedidoRepository
from repositories.produto_repository import ProdutoRepository
from models.pedido import Pedido
from models.item_pedido import ItemPedido
from services.email_service import EmailService # Mock service

# --- EXCEÇÕES PERSONALIZADAS ---
# (Ajuda o DEV 1 a tratar erros específicos na rota da API)

class EstoqueInsuficienteError(Exception):
    """Exceção levantada quando o estoque de um produto é insuficiente."""
    pass

class PagamentoRecusadoError(Exception):
    """Exceção levantada quando o Gateway de Pagamento recusa a transação."""
    pass

# --- CLASSE DE SERVIÇO PRINCIPAL (ORQUESTRAÇÃO) ---

class CheckoutService:
    """
    Responsável por orquestrar todo o processo de finalização do pedido.
    Garante a integridade transacional (RNF07.1).
    """

    def __init__(self, 
                 carrinho_repo: CarrinhoRepository,
                 pedido_repo: PedidoRepository,
                 produto_repo: ProdutoRepository,
                 email_service: EmailService,
                 # O Pagamento Gateway é injetado, mas é a interface (Polimorfismo!)
                 pagamento_gateway: GatewayPagamentoBase):
        """Injeção de Dependências (Controle de Inversão): Recebe Repositórios e Interfaces."""
        self.carrinho_repo = carrinho_repo
        self.pedido_repo = pedido_repo
        self.produto_repo = produto_repo
        self.email_service = email_service
        self.pagamento_gateway = pagamento_gateway

    def processar_compra(self, 
                         carrinho_id: int, 
                         dados_pagamento: Dict[str, Any], 
                         endereco_id: int) -> Pedido:
        """
        Orquestra a criação do Pedido de forma atômica (Tudo ou Nada).
        
        Args:
            carrinho_id: ID do carrinho a ser convertido em pedido.
            dados_pagamento: Dados para o Gateway (ex: número do cartão).
            endereco_id: ID do Endereço de entrega selecionado pelo cliente.

        Returns:
            O objeto Pedido criado.
        """
        
        # 1. PRÉ-VALIDAÇÃO (LEITURA DO CARRINHO E CÁLCULO)
        carrinho = self.carrinho_repo.buscar_por_id(carrinho_id)
        if not carrinho or not carrinho.itens:
            raise ValueError("O carrinho está vazio ou é inválido.")
        
        # Calcula o valor total a ser cobrado
        valor_total = carrinho.calcular_total() # Assume que este método está no Model Carrinho
        
        # 2. INICIAR TRANSAÇÃO (RNF07.1)
        # O PedidoRepository é responsável por abrir a conexão e a transação SQLite
        conexao = self.pedido_repo.iniciar_transacao() 
        
        try:
            # 3. VERIFICAR, BLOQUEAR E ABATER ESTOQUE (RNF07.3 - Concorrência)
            itens_pedido = []
            
            for item_carrinho in carrinho.itens:
                # O ProdutoRepository deve buscar o item DENTRO desta conexão 
                # para garantir que o abate seja seguro.
                produto = self.produto_repo.buscar_por_id_para_bloqueio(item_carrinho.produto_id, conexao) 
                
                if produto.estoque < item_carrinho.quantidade:
                    # Se falhar, levanta exceção para forçar o ROLLBACK no 'finally'
                    raise EstoqueInsuficienteError(f"Estoque insuficiente para {produto.nome}.")
                
                # Abate o estoque no objeto (e a alteração será salva no DB)
                produto.estoque -= item_carrinho.quantidade
                self.produto_repo.atualizar_estoque(produto, conexao) # Persiste o abate

                # Constrói o ItemPedido
                item_pedido = ItemPedido(
                    produto_id=produto.id,
                    quantidade=item_carrinho.quantidade,
                    preco_unitario=produto.preco # Garante o preço daquele momento
                )
                itens_pedido.append(item_pedido)

            # 4. PROCESSAR PAGAMENTO (POLIMORFISMO)
            # Chama a interface sem se importar se é Cartão ou Pix
            pagamento_status = self.pagamento_gateway.processar_pagamento(
                valor_total, 
                dados_pagamento
            )

            # 5. VERIFICAR STATUS DO PAGAMENTO
            if pagamento_status == StatusPagamento.REJEITADO:
                raise PagamentoRecusadoError("Pagamento recusado pela operadora.")
            
            # 6. CRIAR REGISTRO DO PEDIDO
            
            # Define o status inicial baseado na resposta do pagamento
            if pagamento_status == StatusPagamento.APROVADO:
                status_final = StatusPedido.PROCESSANDO
            else: # PENDENTE (Pix, Boleto)
                status_final = StatusPedido.PAGAMENTO_PENDENTE 

            novo_pedido = Pedido(
                cliente_id=carrinho.cliente_id,
                endereco_entrega_id=endereco_id,
                valor_total=valor_total,
                status=status_final,
                itens=itens_pedido
            )
            
            # Salva Pedido e ItensPedido no DB, usando a conexão transacional
            self.pedido_repo.salvar_pedido_e_itens(novo_pedido, conexao)

            # 7. FINALIZAR TRANSAÇÃO COM SUCESSO (COMMIT)
            self.pedido_repo.commit_transacao(conexao) 
            
            # 8. AÇÕES PÓS-TRANSAÇÃO (Não precisam de rollback se falharem)
            self.carrinho_repo.limpar_carrinho(carrinho_id)
            self.email_service.enviar_confirmacao(novo_pedido)

            return novo_pedido

        except (EstoqueInsuficienteError, PagamentoRecusadoError, Exception) as e:
            # 9. REVERTER TRANSAÇÃO (ROLLBACK)
            print(f"Erro no checkout: {e}. Executando ROLLBACK.")
            self.pedido_repo.rollback_transacao(conexao) 
            # Relança a exceção para que a rota da API (DEV 1) possa notificar o cliente
            raise e