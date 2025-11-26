"""Serviço de gerenciamento de carrinho de compras.

Implementa lógica de negócio para operações de carrinho com validações
básicas e avançadas de estoque, preços, limites e integridade.
"""
from typing import List, Dict, Any, Optional
from decimal import Decimal
from src.repositories.cart_repository import CarrinhoRepository
from src.repositories.product_repository import ProdutoRepository


class CarrinhoServiceError(Exception):
    """Exceção base para erros do CarrinhoService."""
    pass


class ProdutoIndisponivelError(CarrinhoServiceError):
    """Produto não está disponível para venda."""
    pass


class EstoqueInsuficienteError(CarrinhoServiceError):
    """Quantidade solicitada excede estoque disponível."""
    pass


class LimiteCarrinhoExcedidoError(CarrinhoServiceError):
    """Limite de itens ou valor do carrinho excedido."""
    pass


class PrecoInvalidoError(CarrinhoServiceError):
    """Preço do produto é inválido ou foi alterado."""
    pass


class CarrinhoService:
    """Serviço para gerenciamento de carrinho de compras."""
    
    # Constantes de validação
    MAX_QUANTIDADE_POR_ITEM = 100
    MAX_ITENS_CARRINHO = 50
    MAX_VALOR_CARRINHO = Decimal('50000.00')
    MIN_QUANTIDADE = 1
    
    def __init__(
        self,
        carrinho_repo: CarrinhoRepository,
        produto_repo: ProdutoRepository
    ):
        """Inicializa o serviço com os repositórios necessários.
        
        Args:
            carrinho_repo: Repositório de carrinhos
            produto_repo: Repositório de produtos
        """
        self.carrinho_repo = carrinho_repo
        self.produto_repo = produto_repo
    
    def obter_ou_criar_carrinho(self, usuario_id: int) -> Dict[str, Any]:
        """Obtém o carrinho do usuário ou cria um novo.
        
        Args:
            usuario_id: ID do usuário
            
        Returns:
            Dados do carrinho
            
        Raises:
            CarrinhoServiceError: Se houver erro ao obter/criar carrinho
        """
        if usuario_id <= 0:
            raise CarrinhoServiceError("ID de usuário inválido")
        
        try:
            carrinho = self.carrinho_repo.obter_ou_criar(usuario_id)
            return carrinho
        except Exception as e:
            raise CarrinhoServiceError(f"Erro ao obter carrinho: {str(e)}")
    
    def adicionar_item(
        self,
        usuario_id: int,
        produto_id: int,
        quantidade: int
    ) -> Dict[str, Any]:
        """Adiciona um item ao carrinho com validações completas.
        
        Args:
            usuario_id: ID do usuário
            produto_id: ID do produto
            quantidade: Quantidade a adicionar
            
        Returns:
            Item adicionado ao carrinho
            
        Raises:
            CarrinhoServiceError: Validações básicas
            ProdutoIndisponivelError: Produto inativo ou inexistente
            EstoqueInsuficienteError: Estoque insuficiente
            LimiteCarrinhoExcedidoError: Limites excedidos
        """
        # Validações básicas
        self._validar_quantidade(quantidade)
        
        # Buscar produto
        produto = self.produto_repo.buscar_por_id(produto_id)
        if not produto:
            raise ProdutoIndisponivelError(f"Produto {produto_id} não encontrado")
        
        # Validar disponibilidade do produto
        self._validar_produto_disponivel(produto)
        
        # Obter carrinho
        carrinho = self.obter_ou_criar_carrinho(usuario_id)
        
        # Validar limites do carrinho
        self._validar_limite_itens(carrinho['id'])
        
        # Validar estoque
        self._validar_estoque(produto, quantidade, carrinho['id'])
        
        # Validar valor total do carrinho após adição
        preco_unitario = Decimal(str(produto['preco']))
        self._validar_valor_carrinho(carrinho['id'], quantidade, preco_unitario)
        
        # Adicionar item
        try:
            item = self.carrinho_repo.adicionar_item(
                carrinho['id'],
                produto_id,
                quantidade,
                float(preco_unitario)
            )
            return item
        except Exception as e:
            raise CarrinhoServiceError(f"Erro ao adicionar item: {str(e)}")
    
    def remover_item(self, usuario_id: int, item_id: int) -> bool:
        """Remove um item do carrinho.
        
        Args:
            usuario_id: ID do usuário
            item_id: ID do item a remover
            
        Returns:
            True se removido com sucesso
            
        Raises:
            CarrinhoServiceError: Se houver erro na remoção
        """
        # Validar que o item pertence ao usuário
        carrinho = self.obter_ou_criar_carrinho(usuario_id)
        itens = self.carrinho_repo.listar_itens(carrinho['id'])
        
        item_existe = any(item['id'] == item_id for item in itens)
        if not item_existe:
            raise CarrinhoServiceError("Item não encontrado no carrinho")
        
        try:
            return self.carrinho_repo.remover_item(item_id)
        except Exception as e:
            raise CarrinhoServiceError(f"Erro ao remover item: {str(e)}")
    
    def atualizar_quantidade(
        self,
        usuario_id: int,
        item_id: int,
        nova_quantidade: int
    ) -> bool:
        """Atualiza a quantidade de um item no carrinho.
        
        Args:
            usuario_id: ID do usuário
            item_id: ID do item
            nova_quantidade: Nova quantidade
            
        Returns:
            True se atualizado com sucesso
            
        Raises:
            CarrinhoServiceError: Validações básicas
            EstoqueInsuficienteError: Estoque insuficiente
        """
        # Validar quantidade
        if nova_quantidade < 0:
            raise CarrinhoServiceError("Quantidade não pode ser negativa")
        
        if nova_quantidade == 0:
            return self.remover_item(usuario_id, item_id)
        
        self._validar_quantidade(nova_quantidade)
        
        # Buscar item e produto
        carrinho = self.obter_ou_criar_carrinho(usuario_id)
        itens = self.carrinho_repo.listar_itens(carrinho['id'])
        
        item = next((i for i in itens if i['id'] == item_id), None)
        if not item:
            raise CarrinhoServiceError("Item não encontrado no carrinho")
        
        # Validar estoque para nova quantidade
        produto = self.produto_repo.buscar_por_id(item['produto_id'])
        if not produto:
            raise CarrinhoServiceError("Produto não encontrado")
        
        self._validar_produto_disponivel(produto)
        
        # Calcular diferença de quantidade
        diferenca = nova_quantidade - item['quantidade']
        if diferenca > 0:
            self._validar_estoque(produto, diferenca, carrinho['id'], item_id)
        
        try:
            return self.carrinho_repo.atualizar_quantidade_item(item_id, nova_quantidade)
        except Exception as e:
            raise CarrinhoServiceError(f"Erro ao atualizar quantidade: {str(e)}")
    
    def listar_itens(self, usuario_id: int) -> List[Dict[str, Any]]:
        """Lista todos os itens do carrinho do usuário.
        
        Args:
            usuario_id: ID do usuário
            
        Returns:
            Lista de itens com detalhes dos produtos
        """
        carrinho = self.obter_ou_criar_carrinho(usuario_id)
        return self.carrinho_repo.listar_itens(carrinho['id'])
    
    def calcular_total(self, usuario_id: int) -> Decimal:
        """Calcula o valor total do carrinho.
        
        Args:
            usuario_id: ID do usuário
            
        Returns:
            Valor total do carrinho
        """
        carrinho = self.obter_ou_criar_carrinho(usuario_id)
        total = self.carrinho_repo.calcular_total(carrinho['id'])
        return Decimal(str(total))
    
    def limpar_carrinho(self, usuario_id: int) -> bool:
        """Remove todos os itens do carrinho.
        
        Args:
            usuario_id: ID do usuário
            
        Returns:
            True se itens foram removidos
        """
        carrinho = self.obter_ou_criar_carrinho(usuario_id)
        return self.carrinho_repo.limpar(carrinho['id'])
    
    def validar_carrinho_para_compra(self, usuario_id: int) -> Dict[str, Any]:
        """Valida se o carrinho está pronto para checkout.
        
        Args:
            usuario_id: ID do usuário
            
        Returns:
            Dicionário com status da validação e mensagens
            
        Raises:
            CarrinhoServiceError: Se carrinho estiver vazio
        """
        itens = self.listar_itens(usuario_id)
        
        if not itens:
            raise CarrinhoServiceError("Carrinho está vazio")
        
        erros = []
        avisos = []
        
        for item in itens:
            produto = self.produto_repo.buscar_por_id(item['produto_id'])
            
            # Validar existência
            if not produto:
                erros.append(f"Produto '{item['produto_nome']}' não existe mais")
                continue
            
            # Validar disponibilidade
            if not produto.get('ativo', False):
                erros.append(f"Produto '{produto['nome']}' não está mais disponível")
                continue
            
            # Validar estoque
            if produto['estoque'] < item['quantidade']:
                erros.append(
                    f"Estoque insuficiente para '{produto['nome']}'. "
                    f"Disponível: {produto['estoque']}, solicitado: {item['quantidade']}"
                )
            
            # Validar preço
            preco_atual = Decimal(str(produto['preco']))
            preco_carrinho = Decimal(str(item['preco_unitario']))
            
            if preco_atual != preco_carrinho:
                avisos.append(
                    f"Preço de '{produto['nome']}' foi atualizado. "
                    f"Anterior: R$ {preco_carrinho:.2f}, atual: R$ {preco_atual:.2f}"
                )
        
        return {
            'valido': len(erros) == 0,
            'erros': erros,
            'avisos': avisos,
            'total_itens': len(itens),
            'valor_total': float(self.calcular_total(usuario_id))
        }
    
    # Métodos privados de validação
    
    def _validar_quantidade(self, quantidade: int) -> None:
        """Valida se a quantidade está dentro dos limites."""
        if quantidade < self.MIN_QUANTIDADE:
            raise CarrinhoServiceError(
                f"Quantidade mínima é {self.MIN_QUANTIDADE}"
            )
        
        if quantidade > self.MAX_QUANTIDADE_POR_ITEM:
            raise LimiteCarrinhoExcedidoError(
                f"Quantidade máxima por item é {self.MAX_QUANTIDADE_POR_ITEM}"
            )
    
    def _validar_produto_disponivel(self, produto: Dict[str, Any]) -> None:
        """Valida se o produto está disponível para venda."""
        if not produto.get('ativo', False):
            raise ProdutoIndisponivelError(
                f"Produto '{produto['nome']}' não está disponível"
            )
    
    def _validar_estoque(
        self,
        produto: Dict[str, Any],
        quantidade: int,
        carrinho_id: int,
        item_id_excluir: Optional[int] = None
    ) -> None:
        """Valida se há estoque suficiente.
        
        Args:
            produto: Dados do produto
            quantidade: Quantidade solicitada
            carrinho_id: ID do carrinho
            item_id_excluir: ID do item a excluir da verificação (para updates)
        """
        # Buscar quantidade já no carrinho
        itens = self.carrinho_repo.listar_itens(carrinho_id)
        quantidade_no_carrinho = sum(
            item['quantidade']
            for item in itens
            if item['produto_id'] == produto['id'] and item['id'] != item_id_excluir
        )
        
        quantidade_total_necessaria = quantidade_no_carrinho + quantidade
        
        if quantidade_total_necessaria > produto['estoque']:
            raise EstoqueInsuficienteError(
                f"Estoque insuficiente para '{produto['nome']}'. "
                f"Disponível: {produto['estoque']}, "
                f"já no carrinho: {quantidade_no_carrinho}, "
                f"solicitado: {quantidade}"
            )
    
    def _validar_limite_itens(self, carrinho_id: int) -> None:
        """Valida se o número de itens não excede o limite."""
        itens = self.carrinho_repo.listar_itens(carrinho_id)
        
        if len(itens) >= self.MAX_ITENS_CARRINHO:
            raise LimiteCarrinhoExcedidoError(
                f"Limite de {self.MAX_ITENS_CARRINHO} itens no carrinho atingido"
            )
    
    def _validar_valor_carrinho(
        self,
        carrinho_id: int,
        quantidade_adicional: int,
        preco_unitario: Decimal
    ) -> None:
        """Valida se o valor total não excede o limite."""
        total_atual = Decimal(str(self.carrinho_repo.calcular_total(carrinho_id)))
        valor_adicional = preco_unitario * quantidade_adicional
        novo_total = total_atual + valor_adicional
        
        if novo_total > self.MAX_VALOR_CARRINHO:
            raise LimiteCarrinhoExcedidoError(
                f"Valor máximo do carrinho (R$ {self.MAX_VALOR_CARRINHO:.2f}) "
                f"seria excedido. Total atual: R$ {total_atual:.2f}"
            )
