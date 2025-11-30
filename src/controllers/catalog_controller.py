"""
CatalogController - Controlador de Catálogo
==========================================

Gerencia produtos, categorias e navegação no catálogo.
"""
from typing import Dict, Any, List, Optional
from src.controllers.base_controller import BaseController
from src.services.catalog_service import CatalogService
from src.models.products.product_model import Produto
from src.models.products.category_model import Categoria


class CatalogController(BaseController):
    """
    Controller para operações de catálogo.
    
    Métodos:
    - list_products(): Lista produtos
    - list_categories(): Lista categorias
    - get_product_details(): Detalhes de produto
    - filter_by_category(): Filtra por categoria
    - search_products(): Busca produtos
    """
    
    def __init__(self, main_window):
        super().__init__(main_window)
        self.catalog_service = CatalogService()
    
    def list_products(self, categoria_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Lista produtos (opcionalmente filtrados por categoria).
        
        Args:
            categoria_id: ID da categoria para filtrar (None = todos)
            
        Returns:
            Dicionário com success, message e data (lista de produtos)
        """
        try:
            produtos = self.catalog_service.listar_produtos()
            
            # Filtrar por categoria se especificado
            if categoria_id:
                produtos = [
                    p for p in produtos
                    if p.categoria and p.categoria.id == categoria_id
                ]
            
            # Filtrar apenas produtos ativos
            produtos_ativos = [p for p in produtos if p.ativo]
            
            return self._success_response(
                f'{len(produtos_ativos)} produto(s) encontrado(s)',
                produtos_ativos
            )
        
        except Exception as e:
            return self._error_response(
                'Erro ao listar produtos',
                e
            )
    
    def list_categories(self) -> Dict[str, Any]:
        """
        Lista todas as categorias.
        
        Returns:
            Dicionário com success, message e data (lista de categorias)
        """
        try:
            categorias = self.catalog_service.listar_categorias()
            
            return self._success_response(
                f'{len(categorias)} categoria(s) encontrada(s)',
                categorias
            )
        
        except Exception as e:
            return self._error_response(
                'Erro ao listar categorias',
                e
            )
    
    def get_product_details(self, produto_id: int) -> Dict[str, Any]:
        """
        Obtém detalhes de um produto.
        
        Args:
            produto_id: ID do produto
            
        Returns:
            Dicionário com success, message e data (produto)
        """
        try:
            produtos = self.catalog_service.listar_produtos()
            produto = next(
                (p for p in produtos if p.id == produto_id),
                None
            )
            
            if not produto:
                return self._error_response('Produto não encontrado')
            
            return self._success_response(
                'Produto encontrado',
                produto
            )
        
        except Exception as e:
            return self._error_response(
                'Erro ao buscar produto',
                e
            )
    
    def search_products(self, termo: str) -> Dict[str, Any]:
        """
        Busca produtos por nome ou descrição.
        
        Args:
            termo: Termo de busca
            
        Returns:
            Dicionário com success, message e data (lista de produtos)
        """
        if not termo or not termo.strip():
            return self._error_response('Digite um termo para buscar')
        
        try:
            produtos = self.catalog_service.listar_produtos()
            termo_lower = termo.lower().strip()
            
            # Buscar em nome e descrição
            resultados = [
                p for p in produtos
                if (termo_lower in p.nome.lower() or
                    termo_lower in (p.descricao or '').lower())
                and p.ativo
            ]
            
            return self._success_response(
                f'{len(resultados)} produto(s) encontrado(s)',
                resultados
            )
        
        except Exception as e:
            return self._error_response(
                'Erro ao buscar produtos',
                e
            )
    
    def view_product_details(self, produto_id: int) -> Dict[str, Any]:
        """
        Navega para a tela de detalhes do produto.
        
        Args:
            produto_id: ID do produto
            
        Returns:
            Dicionário com success e message
        """
        result = self.get_product_details(produto_id)
        
        if result['success']:
            self.navigate_to('ProductDetailView', result['data'])
        
        return result
