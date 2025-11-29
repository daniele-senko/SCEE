"""Testes para o CatalogService."""
import pytest
from src.services.catalog_service import CatalogService
from src.models.products.category_model import Categoria
from src.models.products.product_model import Produto


class TestCatalogService:
    """Testes do serviço de catálogo."""
    
    def test_listar_categorias(self, db_connection):
        """Testa listagem de categorias."""
        service = CatalogService()
        
        categorias = service.listar_categorias()
        
        assert len(categorias) > 0
        assert all(isinstance(cat, Categoria) for cat in categorias)
        assert any(cat.nome == 'Eletrônicos' for cat in categorias)
    
    def test_listar_produtos(self, db_connection):
        """Testa listagem de produtos."""
        service = CatalogService()
        
        produtos = service.listar_produtos()
        
        assert len(produtos) > 0
        assert all(isinstance(prod, Produto) for prod in produtos)
        # Verifica se tem produto do seeder
        assert any(prod.nome == 'Fone de Ouvido Bluetooth' for prod in produtos)
    
    def test_listar_produtos_com_categoria(self, db_connection):
        """Testa que produtos têm categoria vinculada."""
        service = CatalogService()
        
        produtos = service.listar_produtos()
        
        # Verifica se pelo menos um produto tem categoria
        produtos_com_categoria = [p for p in produtos if p.categoria is not None]
        assert len(produtos_com_categoria) > 0
        
        # Verifica tipo da categoria
        primeiro_com_cat = produtos_com_categoria[0]
        assert isinstance(primeiro_com_cat.categoria, Categoria)
    
    def test_cadastrar_produto_sucesso(self, db_connection):
        """Testa cadastro de novo produto."""
        service = CatalogService()
        
        # Cadastrar produto na categoria Eletrônicos (existe no seeder)
        service.cadastrar_produto(
            nome="Produto Teste",
            sku="TEST-001",
            preco=99.90,
            estoque=10,
            nome_categoria="Eletrônicos"
        )
        
        # Verificar se foi criado
        produtos = service.listar_produtos()
        assert any(p.nome == "Produto Teste" for p in produtos)
    
    def test_cadastrar_produto_categoria_invalida(self, db_connection):
        """Testa erro ao cadastrar produto com categoria inválida."""
        service = CatalogService()
        
        with pytest.raises(ValueError, match="Categoria.*inválida"):
            service.cadastrar_produto(
                nome="Produto Teste",
                sku="TEST-001",
                preco=99.90,
                estoque=10,
                nome_categoria="Categoria Inexistente"
            )
    
    def test_remover_produto(self, db_connection):
        """Testa remoção de produto."""
        service = CatalogService()
        
        # Cadastrar produto
        service.cadastrar_produto(
            nome="Produto Para Remover",
            sku="REMOVE-001",
            preco=50.00,
            estoque=5,
            nome_categoria="Eletrônicos"
        )
        
        # Buscar ID do produto criado
        produtos = service.listar_produtos()
        produto = next(p for p in produtos if p.nome == "Produto Para Remover")
        
        # Remover
        resultado = service.remover_produto(produto.id)
        
        assert resultado is True
