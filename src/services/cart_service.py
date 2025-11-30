"""Serviço de gerenciamento de carrinho de compras."""
from typing import List, Dict, Any, Optional
from decimal import Decimal
from src.repositories.cart_repository import CarrinhoRepository
from src.repositories.product_repository import ProductRepository

class CarrinhoServiceError(Exception): pass
class ProdutoIndisponivelError(CarrinhoServiceError): pass
class EstoqueInsuficienteError(CarrinhoServiceError): pass
class LimiteCarrinhoExcedidoError(CarrinhoServiceError): pass
class PrecoInvalidoError(CarrinhoServiceError): pass

class CarrinhoService:
    
    # Constantes
    MAX_QUANTIDADE_POR_ITEM = 100
    MAX_ITENS_CARRINHO = 50
    MAX_VALOR_CARRINHO = Decimal('50000.00')
    MIN_QUANTIDADE = 1
    
    def __init__(self, carrinho_repo: CarrinhoRepository, produto_repo: ProductRepository):
        self.carrinho_repo = carrinho_repo
        self.produto_repo = produto_repo
    
    def obter_ou_criar_carrinho(self, usuario_id: int) -> Dict[str, Any]:
        if usuario_id <= 0:
            raise CarrinhoServiceError("ID de usuário inválido")
        try:
            return self.carrinho_repo.obter_ou_criar(usuario_id)
        except Exception as e:
            raise CarrinhoServiceError(f"Erro ao obter carrinho: {str(e)}")

    # --- Garante dados completos para a View ---
    def obter_carrinho_completo(self, usuario_id: int) -> Dict[str, Any]:
        """Retorna carrinho com itens e total calculado."""
        # 1. Garante que carrinho existe
        carrinho = self.obter_ou_criar_carrinho(usuario_id)
        carrinho_id = carrinho['id']
        
        # 2. Busca itens
        itens = self.carrinho_repo.listar_itens(carrinho_id)
        carrinho['itens'] = itens
        
        # 3. Calcula total
        total = self.carrinho_repo.calcular_total(carrinho_id)
        carrinho['total'] = float(total)
        carrinho['quantidade_itens'] = len(itens)
        
        return carrinho

    def adicionar_item(self, usuario_id: int, produto_id: int, quantidade: int) -> Dict[str, Any]:
        self._validar_quantidade(quantidade)
        
        produto = self.produto_repo.buscar_por_id(produto_id)
        if not produto:
            raise ProdutoIndisponivelError(f"Produto {produto_id} não encontrado")
        
        self._validar_produto_disponivel(produto)
        carrinho = self.obter_ou_criar_carrinho(usuario_id)
        self._validar_limite_itens(carrinho['id'])
        self._validar_estoque(produto, quantidade, carrinho['id'])
        
        preco_unitario = Decimal(str(produto['preco']))
        self._validar_valor_carrinho(carrinho['id'], quantidade, preco_unitario)
        
        try:
            return self.carrinho_repo.adicionar_item(
                carrinho['id'], produto_id, quantidade, float(preco_unitario)
            )
        except Exception as e:
            raise CarrinhoServiceError(f"Erro ao adicionar item: {str(e)}")
    
    def remover_item(self, usuario_id: int, item_id: int) -> bool:
        # Apenas verifica se o carrinho existe para o usuário, mas remove pelo ID do item
        self.obter_ou_criar_carrinho(usuario_id)
        try:
            return self.carrinho_repo.remover_item(item_id)
        except Exception as e:
            raise CarrinhoServiceError(f"Erro ao remover item: {str(e)}")
    
    def atualizar_quantidade(self, usuario_id: int, item_id: int, nova_quantidade: int) -> bool:
        if nova_quantidade == 0:
            return self.remover_item(usuario_id, item_id)
        
        self._validar_quantidade(nova_quantidade)
        carrinho = self.obter_ou_criar_carrinho(usuario_id)
        
        # Busca item para validar estoque
        itens = self.carrinho_repo.listar_itens(carrinho['id'])
        item = next((i for i in itens if i['id'] == item_id), None)
        
        if item:
            produto = self.produto_repo.buscar_por_id(item['produto_id'])
            diferenca = nova_quantidade - item['quantidade']
            if diferenca > 0:
                self._validar_estoque(produto, diferenca, carrinho['id'], item_id)

        try:
            return self.carrinho_repo.atualizar_quantidade_item(item_id, nova_quantidade)
        except Exception as e:
            raise CarrinhoServiceError(f"Erro ao atualizar: {str(e)}")

    def listar_itens(self, usuario_id: int) -> List[Dict[str, Any]]:
        carrinho = self.obter_ou_criar_carrinho(usuario_id)
        return self.carrinho_repo.listar_itens(carrinho['id'])
    
    def calcular_total(self, usuario_id: int) -> Decimal:
        carrinho = self.obter_ou_criar_carrinho(usuario_id)
        total = self.carrinho_repo.calcular_total(carrinho['id'])
        return Decimal(str(total))
    
    def limpar_carrinho(self, carrinho_id: int) -> bool:
        return self.carrinho_repo.limpar(carrinho_id)

    # --- Validações Privadas ---
    def _validar_quantidade(self, quantidade: int):
        if quantidade < self.MIN_QUANTIDADE:
            raise CarrinhoServiceError(f"Qtd mínima: {self.MIN_QUANTIDADE}")
        if quantidade > self.MAX_QUANTIDADE_POR_ITEM:
            raise LimiteCarrinhoExcedidoError(f"Qtd máxima: {self.MAX_QUANTIDADE_POR_ITEM}")

    def _validar_produto_disponivel(self, produto):
        if not produto.get('ativo', False):
            raise ProdutoIndisponivelError("Produto indisponível")

    def _validar_estoque(self, produto, quantidade, carrinho_id, item_id_excluir=None):
        # Simplificação: Validação direta
        if produto['estoque'] < quantidade:
             raise EstoqueInsuficienteError(f"Estoque insuficiente: {produto['nome']}")

    def _validar_limite_itens(self, carrinho_id):
        pass # Implementar se necessário

    def _validar_valor_carrinho(self, carrinho_id, qtd, preco):
        pass # Implementar se necessário