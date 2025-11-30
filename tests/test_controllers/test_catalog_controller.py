"""
Testes para CatalogController
==============================

Testa operações de catálogo de produtos.
"""
import pytest
from unittest.mock import Mock, patch
from src.controllers.catalog_controller import CatalogController


@pytest.fixture
def mock_main_window():
    """Mock da MainWindow."""
    window = Mock()
    window.show_view = Mock()
    return window


@pytest.fixture
def controller(mock_main_window):
    """Fixture do CatalogController."""
    return CatalogController(mock_main_window)


@pytest.fixture
def categorias_mock():
    """Categorias mock."""
    return [
        Mock(id=1, nome="Eletrônicos"),
        Mock(id=2, nome="Livros")
    ]


@pytest.fixture
def produtos_mock(categorias_mock):
    """Produtos mock."""
    # Criar mocks com atributos configuráveis
    p1 = Mock()
    p1.id = 1
    p1.nome = "Notebook"
    p1.sku = "NB001"
    p1.preco = 2500.00
    p1.estoque = 10
    p1.categoria = categorias_mock[0]
    p1.ativo = True
    p1.descricao = "Notebook Dell"
    
    p2 = Mock()
    p2.id = 2
    p2.nome = "Mouse"
    p2.sku = "MS001"
    p2.preco = 50.00
    p2.estoque = 20
    p2.categoria = categorias_mock[0]
    p2.ativo = True
    p2.descricao = "Mouse sem fio"
    
    p3 = Mock()
    p3.id = 3
    p3.nome = "Livro Python"
    p3.sku = "LV001"
    p3.preco = 80.00
    p3.estoque = 15
    p3.categoria = categorias_mock[1]
    p3.ativo = True
    p3.descricao = "Livro de Python"
    
    p4 = Mock()
    p4.id = 4
    p4.nome = "Produto Inativo"
    p4.sku = "IN001"
    p4.preco = 100.00
    p4.estoque = 0
    p4.categoria = categorias_mock[0]
    p4.ativo = False
    p4.descricao = "Produto descontinuado"
    
    return [p1, p2, p3, p4]


class TestCatalogControllerListProducts:
    """Testes de listar produtos."""
    
    def test_list_products_todos(self, controller, produtos_mock):
        """Deve listar todos os produtos ativos."""
        with patch.object(controller.catalog_service, 'listar_produtos', return_value=produtos_mock):
            result = controller.list_products()
        
        assert result['success']
        assert len(result['data']) == 3  # Apenas ativos
        assert '3 produto(s)' in result['message']
    
    def test_list_products_filtrar_por_categoria(self, controller, produtos_mock):
        """Deve filtrar produtos por categoria."""
        with patch.object(controller.catalog_service, 'listar_produtos', return_value=produtos_mock):
            result = controller.list_products(categoria_id=1)
        
        assert result['success']
        assert len(result['data']) == 2  # Notebook e Mouse (ativos) da categoria 1
    
    def test_list_products_categoria_sem_produtos(self, controller, produtos_mock):
        """Deve retornar vazio para categoria sem produtos."""
        with patch.object(controller.catalog_service, 'listar_produtos', return_value=produtos_mock):
            result = controller.list_products(categoria_id=999)
        
        assert result['success']
        assert len(result['data']) == 0
    
    def test_list_products_exception(self, controller):
        """Deve tratar exceção ao listar produtos."""
        with patch.object(controller.catalog_service, 'listar_produtos',
                         side_effect=Exception("DB Error")):
            result = controller.list_products()
        
        assert not result['success']
        assert 'Erro ao listar produtos' in result['message']


class TestCatalogControllerListCategories:
    """Testes de listar categorias."""
    
    def test_list_categories_sucesso(self, controller, categorias_mock):
        """Deve listar categorias com sucesso."""
        with patch.object(controller.catalog_service, 'listar_categorias', return_value=categorias_mock):
            result = controller.list_categories()
        
        assert result['success']
        assert len(result['data']) == 2
        assert '2 categoria(s)' in result['message']
    
    def test_list_categories_vazia(self, controller):
        """Deve retornar lista vazia."""
        with patch.object(controller.catalog_service, 'listar_categorias', return_value=[]):
            result = controller.list_categories()
        
        assert result['success']
        assert len(result['data']) == 0
    
    def test_list_categories_exception(self, controller):
        """Deve tratar exceção ao listar categorias."""
        with patch.object(controller.catalog_service, 'listar_categorias',
                         side_effect=Exception("Error")):
            result = controller.list_categories()
        
        assert not result['success']


class TestCatalogControllerProductDetails:
    """Testes de detalhes de produto."""
    
    def test_get_product_details_sucesso(self, controller, produtos_mock):
        """Deve obter detalhes do produto."""
        with patch.object(controller.catalog_service, 'listar_produtos', return_value=produtos_mock):
            result = controller.get_product_details(1)
        
        assert result['success']
        assert result['data'].id == 1
        assert result['data'].nome == "Notebook"
    
    def test_get_product_details_nao_encontrado(self, controller, produtos_mock):
        """Deve falhar quando produto não existe."""
        with patch.object(controller.catalog_service, 'listar_produtos', return_value=produtos_mock):
            result = controller.get_product_details(999)
        
        assert not result['success']
        assert 'não encontrado' in result['message']
    
    def test_get_product_details_exception(self, controller):
        """Deve tratar exceção."""
        with patch.object(controller.catalog_service, 'listar_produtos',
                         side_effect=Exception("Error")):
            result = controller.get_product_details(1)
        
        assert not result['success']


class TestCatalogControllerSearch:
    """Testes de busca de produtos."""
    
    def test_search_products_termo_vazio(self, controller):
        """Deve falhar com termo vazio."""
        result = controller.search_products("")
        
        assert not result['success']
        assert 'Digite um termo' in result['message']
    
    def test_search_products_por_nome(self, controller, produtos_mock):
        """Deve buscar produtos por nome."""
        with patch.object(controller.catalog_service, 'listar_produtos', return_value=produtos_mock):
            result = controller.search_products("Notebook")
        
        assert result['success']
        assert len(result['data']) >= 1
    
    def test_search_products_case_insensitive(self, controller, produtos_mock):
        """Busca deve ser case-insensitive."""
        with patch.object(controller.catalog_service, 'listar_produtos', return_value=produtos_mock):
            result = controller.search_products("notebook")
        
        assert result['success']
        assert len(result['data']) >= 1
    
    def test_search_products_por_descricao(self, controller, produtos_mock):
        """Deve buscar em descrição também."""
        # Garantir que os mocks têm descricao
        if hasattr(produtos_mock[0], 'descricao'):
            produtos_mock[0].descricao = "Notebook Dell Inspiron"
        
        with patch.object(controller.catalog_service, 'listar_produtos', return_value=produtos_mock):
            result = controller.search_products("Notebook")
        
        assert result['success']
        assert len(result['data']) >= 1
    
    def test_search_products_sem_resultados(self, controller, produtos_mock):
        """Deve retornar vazio quando não encontra."""
        with patch.object(controller.catalog_service, 'listar_produtos', return_value=produtos_mock):
            result = controller.search_products("XYZ9999999")
        
        assert result['success']
        assert len(result['data']) == 0
    
    def test_search_products_nao_retorna_inativos(self, controller, produtos_mock):
        """Não deve retornar produtos inativos."""
        # Marcar o último produto como inativo se existir
        if len(produtos_mock) > 3 and hasattr(produtos_mock[3], 'ativo'):
            produtos_mock[3].ativo = False
        
        with patch.object(controller.catalog_service, 'listar_produtos', return_value=produtos_mock):
            result = controller.search_products("Inativo")
        
        assert result['success']
        # Não deve retornar o produto inativo
        assert all(getattr(p, 'ativo', True) for p in result['data'])
    
    def test_search_products_exception(self, controller):
        """Deve tratar exceção na busca."""
        with patch.object(controller.catalog_service, 'listar_produtos',
                         side_effect=Exception("Error")):
            result = controller.search_products("test")
        
        assert not result['success']


class TestCatalogControllerNavigation:
    """Testes de navegação."""
    
    def test_view_product_details_sucesso(self, controller, mock_main_window, produtos_mock):
        """Deve navegar para detalhes do produto."""
        with patch.object(controller.catalog_service, 'listar_produtos', return_value=produtos_mock):
            result = controller.view_product_details(1)
        
        assert result['success']
        mock_main_window.show_view.assert_called_once_with('ProductDetailView', produtos_mock[0])
    
    def test_view_product_details_produto_nao_existe(self, controller, mock_main_window, produtos_mock):
        """Não deve navegar quando produto não existe."""
        with patch.object(controller.catalog_service, 'listar_produtos', return_value=produtos_mock):
            result = controller.view_product_details(999)
        
        assert not result['success']
        mock_main_window.show_view.assert_not_called()
