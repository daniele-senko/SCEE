"""Testes para o CarrinhoService."""
import pytest
from decimal import Decimal
from src.services.cart_service import (
    CarrinhoService,
    CarrinhoServiceError,
    ProdutoIndisponivelError,
    EstoqueInsuficienteError,
    LimiteCarrinhoExcedidoError
)
from src.repositories.cart_repository import CarrinhoRepository
from src.repositories.product_repository import ProductRepository


class TestCarrinhoService:
    """Testes do serviço de carrinho."""
    
    def test_obter_ou_criar_carrinho_sucesso(self, db_connection):
        """Testa criação/obtenção de carrinho."""
        carrinho_repo = CarrinhoRepository()
        produto_repo = ProductRepository()
        service = CarrinhoService(carrinho_repo, produto_repo)
        
        # Cliente ID 2 existe no seeder
        carrinho = service.obter_ou_criar_carrinho(2)
        
        assert carrinho is not None
        assert carrinho['usuario_id'] == 2
        assert 'id' in carrinho
    
    def test_obter_carrinho_usuario_invalido(self, db_connection):
        """Testa erro com usuário inválido."""
        carrinho_repo = CarrinhoRepository()
        produto_repo = ProductRepository()
        service = CarrinhoService(carrinho_repo, produto_repo)
        
        with pytest.raises(CarrinhoServiceError, match="ID de usuário inválido"):
            service.obter_ou_criar_carrinho(0)
    
    def test_adicionar_item_sucesso(self, db_connection):
        """Testa adição de item ao carrinho."""
        carrinho_repo = CarrinhoRepository()
        produto_repo = ProductRepository()
        service = CarrinhoService(carrinho_repo, produto_repo)
        
        # Produto ID 1 existe no seeder (Fone de Ouvido - estoque 50)
        item = service.adicionar_item(
            usuario_id=2,
            produto_id=1,
            quantidade=2
        )
        
        assert item is not None
        assert item['produto_id'] == 1
        assert item['quantidade'] == 2
    
    def test_adicionar_item_quantidade_invalida(self, db_connection):
        """Testa erro ao adicionar quantidade inválida."""
        carrinho_repo = CarrinhoRepository()
        produto_repo = ProductRepository()
        service = CarrinhoService(carrinho_repo, produto_repo)
        
        with pytest.raises(CarrinhoServiceError, match="Quantidade mínima"):
            service.adicionar_item(2, 1, 0)
    
    def test_adicionar_item_produto_inexistente(self, db_connection):
        """Testa erro ao adicionar produto inexistente."""
        carrinho_repo = CarrinhoRepository()
        produto_repo = ProductRepository()
        service = CarrinhoService(carrinho_repo, produto_repo)
        
        with pytest.raises(ProdutoIndisponivelError, match="não encontrado"):
            service.adicionar_item(2, 99999, 1)
    
    def test_adicionar_item_estoque_insuficiente(self, db_connection):
        """Testa erro quando estoque é insuficiente."""
        carrinho_repo = CarrinhoRepository()
        produto_repo = ProductRepository()
        service = CarrinhoService(carrinho_repo, produto_repo)
        
        # Produto tem estoque 50, tenta adicionar 51
        with pytest.raises(EstoqueInsuficienteError, match="Estoque insuficiente"):
            service.adicionar_item(2, 1, 51)
    
    def test_listar_itens(self, db_connection):
        """Testa listagem de itens do carrinho."""
        carrinho_repo = CarrinhoRepository()
        produto_repo = ProductRepository()
        service = CarrinhoService(carrinho_repo, produto_repo)
        
        # Adicionar item
        service.adicionar_item(2, 1, 2)
        
        # Listar
        itens = service.listar_itens(2)
        
        assert len(itens) >= 1
        assert any(item['produto_id'] == 1 for item in itens)
    
    def test_calcular_total(self, db_connection):
        """Testa cálculo do total do carrinho."""
        carrinho_repo = CarrinhoRepository()
        produto_repo = ProductRepository()
        service = CarrinhoService(carrinho_repo, produto_repo)
        
        # Adicionar item (Fone - R$ 199.90)
        service.adicionar_item(2, 1, 2)
        
        # Calcular total
        total = service.calcular_total(2)
        
        assert isinstance(total, Decimal)
        assert total > 0
    
    def test_limpar_carrinho(self, db_connection):
        """Testa limpeza do carrinho."""
        carrinho_repo = CarrinhoRepository()
        produto_repo = ProductRepository()
        service = CarrinhoService(carrinho_repo, produto_repo)
        
        # Adicionar item
        service.adicionar_item(2, 1, 1)
        
        # Limpar
        resultado = service.limpar_carrinho(2)
        
        assert resultado is True
        
        # Verificar se está vazio
        itens = service.listar_itens(2)
        assert len(itens) == 0
    
    def test_validar_carrinho_para_compra_vazio(self, db_connection):
        """Testa validação de carrinho vazio."""
        carrinho_repo = CarrinhoRepository()
        produto_repo = ProductRepository()
        service = CarrinhoService(carrinho_repo, produto_repo)
        
        with pytest.raises(CarrinhoServiceError, match="Carrinho está vazio"):
            service.validar_carrinho_para_compra(2)
    
    def test_validar_carrinho_para_compra_valido(self, db_connection):
        """Testa validação de carrinho válido."""
        carrinho_repo = CarrinhoRepository()
        produto_repo = ProductRepository()
        service = CarrinhoService(carrinho_repo, produto_repo)
        
        # Adicionar item
        service.adicionar_item(2, 1, 1)
        
        # Validar
        resultado = service.validar_carrinho_para_compra(2)
        
        assert resultado['valido'] is True
        assert len(resultado['erros']) == 0
        assert resultado['total_itens'] >= 1
