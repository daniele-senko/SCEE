"""Serviço de catálogo de produtos e categorias.

Implementa lógica de negócio para busca, filtros, paginação e validações
de produtos e categorias.
"""
from typing import List, Dict, Any, Optional, Tuple
from decimal import Decimal
from repositories.produto_repository import ProdutoRepository
from repositories.categoria_repository import CategoriaRepository


class CatalogoServiceError(Exception):
    """Exceção base para erros do CatalogoService."""
    pass


class ProdutoNaoEncontradoError(CatalogoServiceError):
    """Produto não foi encontrado."""
    pass


class CategoriaNaoEncontradaError(CatalogoServiceError):
    """Categoria não foi encontrada."""
    pass


class FiltrosInvalidosError(CatalogoServiceError):
    """Filtros de busca são inválidos."""
    pass


class CatalogoService:
    """Serviço para gerenciamento de catálogo de produtos."""
    
    # Constantes de paginação
    ITENS_POR_PAGINA_PADRAO = 20
    MAX_ITENS_POR_PAGINA = 100
    
    # Constantes de validação
    MIN_PRECO = Decimal('0.01')
    MAX_PRECO = Decimal('999999.99')
    MIN_TERMO_BUSCA = 2
    
    # Ordenações válidas
    ORDENACOES_VALIDAS = {
        'nome_asc': ('nome', 'ASC'),
        'nome_desc': ('nome', 'DESC'),
        'preco_asc': ('preco', 'ASC'),
        'preco_desc': ('preco', 'DESC'),
        'mais_recentes': ('criado_em', 'DESC'),
        'mais_antigos': ('criado_em', 'ASC')
    }
    
    def __init__(
        self,
        produto_repo: ProdutoRepository,
        categoria_repo: CategoriaRepository
    ):
        """Inicializa o serviço com os repositórios necessários.
        
        Args:
            produto_repo: Repositório de produtos
            categoria_repo: Repositório de categorias
        """
        self.produto_repo = produto_repo
        self.categoria_repo = categoria_repo
    
    def buscar_produtos(
        self,
        termo: Optional[str] = None,
        categoria_id: Optional[int] = None,
        preco_min: Optional[float] = None,
        preco_max: Optional[float] = None,
        pagina: int = 1,
        itens_por_pagina: Optional[int] = None,
        apenas_disponiveis: bool = True,
        ordenacao: str = 'nome_asc'
    ) -> Dict[str, Any]:
        """Busca produtos com filtros e paginação.
        
        Args:
            termo: Termo de busca (nome ou descrição)
            categoria_id: Filtrar por categoria
            preco_min: Preço mínimo
            preco_max: Preço máximo
            pagina: Número da página (1-indexed)
            itens_por_pagina: Itens por página
            apenas_disponiveis: Se True, apenas produtos com estoque
            ordenacao: Tipo de ordenação
            
        Returns:
            Dicionário com produtos e metadados de paginação
            
        Raises:
            FiltrosInvalidosError: Filtros inválidos
        """
        # Validar filtros
        self._validar_filtros_busca(
            termo, categoria_id, preco_min, preco_max, pagina, itens_por_pagina
        )
        
        # Determinar itens por página
        if itens_por_pagina is None:
            itens_por_pagina = self.ITENS_POR_PAGINA_PADRAO
        
        # Calcular offset
        offset = (pagina - 1) * itens_por_pagina
        
        # Buscar produtos
        produtos = self.produto_repo.buscar_com_filtros(
            busca=termo,
            categoria_id=categoria_id,
            preco_min=preco_min,
            preco_max=preco_max,
            limit=itens_por_pagina + 1,  # +1 para verificar se há próxima página
            offset=offset
        )
        
        # Filtrar apenas disponíveis
        if apenas_disponiveis:
            produtos = [p for p in produtos if p.get('estoque', 0) > 0]
        
        # Verificar se há mais páginas
        tem_proxima = len(produtos) > itens_por_pagina
        if tem_proxima:
            produtos = produtos[:itens_por_pagina]
        
        # Enriquecer produtos com informações de categoria
        produtos_enriquecidos = []
        for produto in produtos:
            produto_enriquecido = dict(produto)
            if produto.get('categoria_id'):
                categoria = self.categoria_repo.buscar_por_id(produto['categoria_id'])
                if categoria:
                    produto_enriquecido['categoria_nome'] = categoria['nome']
            produtos_enriquecidos.append(produto_enriquecido)
        
        return {
            'produtos': produtos_enriquecidos,
            'paginacao': {
                'pagina_atual': pagina,
                'itens_por_pagina': itens_por_pagina,
                'total_itens_pagina': len(produtos_enriquecidos),
                'tem_proxima': tem_proxima,
                'tem_anterior': pagina > 1
            },
            'filtros_aplicados': {
                'termo': termo,
                'categoria_id': categoria_id,
                'preco_min': preco_min,
                'preco_max': preco_max,
                'apenas_disponiveis': apenas_disponiveis
            }
        }
    
    def buscar_produto_por_id(self, produto_id: int) -> Dict[str, Any]:
        """Busca um produto por ID com informações enriquecidas.
        
        Args:
            produto_id: ID do produto
            
        Returns:
            Produto com informações da categoria
            
        Raises:
            ProdutoNaoEncontradoError: Produto não encontrado
        """
        produto = self.produto_repo.buscar_por_id(produto_id)
        if not produto:
            raise ProdutoNaoEncontradoError(f"Produto {produto_id} não encontrado")
        
        # Enriquecer com categoria
        produto_enriquecido = dict(produto)
        if produto.get('categoria_id'):
            categoria = self.categoria_repo.buscar_por_id(produto['categoria_id'])
            if categoria:
                produto_enriquecido['categoria'] = categoria
        
        # Adicionar metadados
        produto_enriquecido['disponivel'] = (
            produto.get('ativo', False) and produto.get('estoque', 0) > 0
        )
        
        return produto_enriquecido
    
    def buscar_produto_por_sku(self, sku: str) -> Dict[str, Any]:
        """Busca um produto por SKU.
        
        Args:
            sku: SKU do produto
            
        Returns:
            Produto encontrado
            
        Raises:
            ProdutoNaoEncontradoError: Produto não encontrado
        """
        produto = self.produto_repo.buscar_por_sku(sku)
        if not produto:
            raise ProdutoNaoEncontradoError(f"Produto com SKU '{sku}' não encontrado")
        
        return produto
    
    def listar_categorias(self, apenas_ativas: bool = True) -> List[Dict[str, Any]]:
        """Lista todas as categorias.
        
        Args:
            apenas_ativas: Se True, apenas categorias ativas
            
        Returns:
            Lista de categorias com contagem de produtos
        """
        if apenas_ativas:
            categorias = self.categoria_repo.listar_ativas()
        else:
            categorias = self.categoria_repo.listar()
        
        # Adicionar contagem de produtos por categoria
        categorias_enriquecidas = []
        for categoria in categorias:
            categoria_enriquecida = dict(categoria)
            produtos = self.produto_repo.listar_por_categoria(categoria['id'])
            categoria_enriquecida['total_produtos'] = len(produtos)
            categorias_enriquecidas.append(categoria_enriquecida)
        
        return categorias_enriquecidas
    
    def buscar_categoria_por_id(self, categoria_id: int) -> Dict[str, Any]:
        """Busca uma categoria por ID.
        
        Args:
            categoria_id: ID da categoria
            
        Returns:
            Categoria encontrada
            
        Raises:
            CategoriaNaoEncontradaError: Categoria não encontrada
        """
        categoria = self.categoria_repo.buscar_por_id(categoria_id)
        if not categoria:
            raise CategoriaNaoEncontradaError(
                f"Categoria {categoria_id} não encontrada"
            )
        
        return categoria
    
    def listar_produtos_categoria(
        self,
        categoria_id: int,
        pagina: int = 1,
        itens_por_pagina: Optional[int] = None
    ) -> Dict[str, Any]:
        """Lista produtos de uma categoria com paginação.
        
        Args:
            categoria_id: ID da categoria
            pagina: Número da página
            itens_por_pagina: Itens por página
            
        Returns:
            Produtos da categoria com paginação
            
        Raises:
            CategoriaNaoEncontradaError: Categoria não encontrada
        """
        # Verificar se categoria existe
        categoria = self.buscar_categoria_por_id(categoria_id)
        
        # Usar busca com filtro de categoria
        return self.buscar_produtos(
            categoria_id=categoria_id,
            pagina=pagina,
            itens_por_pagina=itens_por_pagina
        )
    
    def validar_disponibilidade(self, produto_id: int, quantidade: int = 1) -> Dict[str, Any]:
        """Valida se um produto está disponível para compra.
        
        Args:
            produto_id: ID do produto
            quantidade: Quantidade desejada
            
        Returns:
            Dicionário com status de disponibilidade
        """
        try:
            produto = self.buscar_produto_por_id(produto_id)
        except ProdutoNaoEncontradoError:
            return {
                'disponivel': False,
                'motivo': 'Produto não encontrado',
                'produto': None
            }
        
        # Verificar se está ativo
        if not produto.get('ativo', False):
            return {
                'disponivel': False,
                'motivo': 'Produto inativo',
                'produto': produto
            }
        
        # Verificar estoque
        estoque = produto.get('estoque', 0)
        if estoque < quantidade:
            return {
                'disponivel': False,
                'motivo': f'Estoque insuficiente (disponível: {estoque})',
                'produto': produto,
                'estoque_disponivel': estoque
            }
        
        return {
            'disponivel': True,
            'motivo': None,
            'produto': produto,
            'estoque_disponivel': estoque
        }
    
    def obter_destaques(self, limite: int = 10) -> List[Dict[str, Any]]:
        """Obtém produtos em destaque (mais recentes com estoque).
        
        Args:
            limite: Número máximo de produtos
            
        Returns:
            Lista de produtos em destaque
        """
        resultado = self.buscar_produtos(
            apenas_disponiveis=True,
            itens_por_pagina=limite,
            ordenacao='mais_recentes'
        )
        return resultado['produtos']
    
    def buscar_relacionados(
        self,
        produto_id: int,
        limite: int = 5
    ) -> List[Dict[str, Any]]:
        """Busca produtos relacionados (mesma categoria).
        
        Args:
            produto_id: ID do produto de referência
            limite: Número máximo de produtos relacionados
            
        Returns:
            Lista de produtos relacionados
        """
        try:
            produto = self.buscar_produto_por_id(produto_id)
        except ProdutoNaoEncontradoError:
            return []
        
        if not produto.get('categoria_id'):
            return []
        
        # Buscar produtos da mesma categoria
        produtos = self.produto_repo.listar_por_categoria(
            produto['categoria_id'],
            limit=limite + 1
        )
        
        # Remover o próprio produto
        relacionados = [p for p in produtos if p['id'] != produto_id][:limite]
        
        return relacionados
    
    def obter_faixa_precos(self) -> Dict[str, float]:
        """Obtém a faixa de preços disponível no catálogo.
        
        Returns:
            Dicionário com preço mínimo e máximo
        """
        produtos = self.produto_repo.listar()
        if not produtos:
            return {'min': 0.0, 'max': 0.0}
        
        precos = [float(p['preco']) for p in produtos if p.get('ativo', False)]
        if not precos:
            return {'min': 0.0, 'max': 0.0}
        
        return {
            'min': min(precos),
            'max': max(precos)
        }
    
    # Métodos privados de validação
    
    def _validar_filtros_busca(
        self,
        termo: Optional[str],
        categoria_id: Optional[int],
        preco_min: Optional[float],
        preco_max: Optional[float],
        pagina: int,
        itens_por_pagina: Optional[int]
    ) -> None:
        """Valida os filtros de busca."""
        # Validar termo de busca
        if termo is not None and len(termo.strip()) < self.MIN_TERMO_BUSCA:
            raise FiltrosInvalidosError(
                f"Termo de busca deve ter pelo menos {self.MIN_TERMO_BUSCA} caracteres"
            )
        
        # Validar categoria
        if categoria_id is not None:
            if categoria_id <= 0:
                raise FiltrosInvalidosError("ID de categoria inválido")
            
            # Verificar se categoria existe
            categoria = self.categoria_repo.buscar_por_id(categoria_id)
            if not categoria:
                raise CategoriaNaoEncontradaError(
                    f"Categoria {categoria_id} não encontrada"
                )
        
        # Validar preços
        if preco_min is not None:
            preco_min_decimal = Decimal(str(preco_min))
            if preco_min_decimal < self.MIN_PRECO:
                raise FiltrosInvalidosError(
                    f"Preço mínimo deve ser pelo menos {self.MIN_PRECO}"
                )
        
        if preco_max is not None:
            preco_max_decimal = Decimal(str(preco_max))
            if preco_max_decimal > self.MAX_PRECO:
                raise FiltrosInvalidosError(
                    f"Preço máximo não pode exceder {self.MAX_PRECO}"
                )
        
        if preco_min is not None and preco_max is not None:
            if preco_min > preco_max:
                raise FiltrosInvalidosError(
                    "Preço mínimo não pode ser maior que preço máximo"
                )
        
        # Validar paginação
        if pagina < 1:
            raise FiltrosInvalidosError("Número de página deve ser maior que zero")
        
        if itens_por_pagina is not None:
            if itens_por_pagina < 1:
                raise FiltrosInvalidosError(
                    "Itens por página deve ser maior que zero"
                )
            if itens_por_pagina > self.MAX_ITENS_POR_PAGINA:
                raise FiltrosInvalidosError(
                    f"Itens por página não pode exceder {self.MAX_ITENS_POR_PAGINA}"
                )
