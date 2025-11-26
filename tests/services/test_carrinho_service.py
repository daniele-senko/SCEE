"""Testes unitários para CarrinhoService.

Para executar:
    python -m pytest tests/services/test_carrinho_service.py -v
    python -m pytest tests/services/test_carrinho_service.py::TestCarrinhoService::test_adicionar_item -v
"""
import pytest
from decimal import Decimal
from unittest.mock import Mock, MagicMock
from src.services.cart_service import (
    CarrinhoService,
    CarrinhoServiceError,
    ProdutoIndisponivelError,
    EstoqueInsuficienteError,
    LimiteCarrinhoExcedidoError
)


class TestCarrinhoService:
    """Testes para o CarrinhoService."""
    
    @pytest.fixture
    def mock_carrinho_repo(self):
        """Mock do CarrinhoRepository."""
        return Mock()
    
    @pytest.fixture
    def mock_produto_repo(self):
        """Mock do ProdutoRepository."""
        return Mock()
    
    @pytest.fixture
    def service(self, mock_carrinho_repo, mock_produto_repo):
        """Instância do CarrinhoService com mocks."""
        return CarrinhoService(mock_carrinho_repo, mock_produto_repo)
    
    @pytest.fixture
    def produto_valido(self):
        """Produto válido para testes."""
        return {
            'id': 1,
            'nome': 'Notebook',
            'preco': 2500.00,
            'estoque': 10,
            'ativo': True
        }
    
    @pytest.fixture
    def carrinho_valido(self):
        """Carrinho válido para testes."""
        return {
            'id': 1,
            'usuario_id': 1,
            'criado_em': '2025-01-01 10:00:00'
        }
    
    # Testes de adicionar_item
    
    def test_adicionar_item_sucesso(self, service, mock_carrinho_repo, mock_produto_repo, produto_valido, carrinho_valido):
        """Testa adição de item com sucesso."""
        # Arrange
        mock_produto_repo.buscar_por_id.return_value = produto_valido
        mock_carrinho_repo.obter_ou_criar.return_value = carrinho_valido
        mock_carrinho_repo.listar_itens.return_value = []
        mock_carrinho_repo.calcular_total.return_value = 0.0
        mock_carrinho_repo.adicionar_item.return_value = {
            'id': 1,
            'carrinho_id': 1,
            'produto_id': 1,
            'quantidade': 2,
            'preco_unitario': 2500.00
        }
        
        # Act
        resultado = service.adicionar_item(usuario_id=1, produto_id=1, quantidade=2)
        
        # Assert
        assert resultado is not None
        assert resultado['quantidade'] == 2
        mock_carrinho_repo.adicionar_item.assert_called_once()
    
    def test_adicionar_item_quantidade_invalida(self, service):
        """Testa adição com quantidade inválida."""
        with pytest.raises(CarrinhoServiceError, match="Quantidade mínima"):
            service.adicionar_item(usuario_id=1, produto_id=1, quantidade=0)
    
    def test_adicionar_item_quantidade_maxima_excedida(self, service):
        """Testa adição excedendo quantidade máxima."""
        with pytest.raises(LimiteCarrinhoExcedidoError, match="Quantidade máxima"):
            service.adicionar_item(usuario_id=1, produto_id=1, quantidade=101)
    
    def test_adicionar_item_produto_nao_encontrado(self, service, mock_produto_repo):
        """Testa adição de produto inexistente."""
        mock_produto_repo.buscar_por_id.return_value = None
        
        with pytest.raises(ProdutoIndisponivelError, match="não encontrado"):
            service.adicionar_item(usuario_id=1, produto_id=999, quantidade=1)
    
    def test_adicionar_item_produto_inativo(self, service, mock_produto_repo, mock_carrinho_repo, carrinho_valido):
        """Testa adição de produto inativo."""
        produto_inativo = {
            'id': 1,
            'nome': 'Notebook',
            'preco': 2500.00,
            'estoque': 10,
            'ativo': False
        }
        mock_produto_repo.buscar_por_id.return_value = produto_inativo
        mock_carrinho_repo.obter_ou_criar.return_value = carrinho_valido
        
        with pytest.raises(ProdutoIndisponivelError, match="não está disponível"):
            service.adicionar_item(usuario_id=1, produto_id=1, quantidade=1)
    
    def test_adicionar_item_estoque_insuficiente(self, service, mock_produto_repo, mock_carrinho_repo, carrinho_valido):
        """Testa adição com estoque insuficiente."""
        produto = {
            'id': 1,
            'nome': 'Notebook',
            'preco': 2500.00,
            'estoque': 2,
            'ativo': True
        }
        mock_produto_repo.buscar_por_id.return_value = produto
        mock_carrinho_repo.obter_ou_criar.return_value = carrinho_valido
        mock_carrinho_repo.listar_itens.return_value = []
        
        with pytest.raises(EstoqueInsuficienteError, match="Estoque insuficiente"):
            service.adicionar_item(usuario_id=1, produto_id=1, quantidade=5)
    
    def test_adicionar_item_limite_itens_excedido(self, service, mock_produto_repo, mock_carrinho_repo, produto_valido, carrinho_valido):
        """Testa adição excedendo limite de itens."""
        mock_produto_repo.buscar_por_id.return_value = produto_valido
        mock_carrinho_repo.obter_ou_criar.return_value = carrinho_valido
        
        # Simula carrinho com 50 itens (limite)
        itens_existentes = [{'id': i, 'produto_id': i, 'quantidade': 1} for i in range(50)]
        mock_carrinho_repo.listar_itens.return_value = itens_existentes
        
        with pytest.raises(LimiteCarrinhoExcedidoError, match="Limite de .* itens"):
            service.adicionar_item(usuario_id=1, produto_id=1, quantidade=1)
    
    # Testes de remover_item
    
    def test_remover_item_sucesso(self, service, mock_carrinho_repo, carrinho_valido):
        """Testa remoção de item com sucesso."""
        mock_carrinho_repo.obter_ou_criar.return_value = carrinho_valido
        mock_carrinho_repo.listar_itens.return_value = [
            {'id': 1, 'produto_id': 1, 'quantidade': 2}
        ]
        mock_carrinho_repo.remover_item.return_value = True
        
        resultado = service.remover_item(usuario_id=1, item_id=1)
        
        assert resultado is True
        mock_carrinho_repo.remover_item.assert_called_once_with(1)
    
    def test_remover_item_nao_encontrado(self, service, mock_carrinho_repo, carrinho_valido):
        """Testa remoção de item inexistente."""
        mock_carrinho_repo.obter_ou_criar.return_value = carrinho_valido
        mock_carrinho_repo.listar_itens.return_value = []
        
        with pytest.raises(CarrinhoServiceError, match="Item não encontrado"):
            service.remover_item(usuario_id=1, item_id=999)
    
    # Testes de atualizar_quantidade
    
    def test_atualizar_quantidade_sucesso(self, service, mock_carrinho_repo, mock_produto_repo, carrinho_valido, produto_valido):
        """Testa atualização de quantidade com sucesso."""
        item_existente = {
            'id': 1,
            'produto_id': 1,
            'quantidade': 2,
            'preco_unitario': 2500.00
        }
        mock_carrinho_repo.obter_ou_criar.return_value = carrinho_valido
        mock_carrinho_repo.listar_itens.return_value = [item_existente]
        mock_produto_repo.buscar_por_id.return_value = produto_valido
        mock_carrinho_repo.atualizar_quantidade_item.return_value = True
        
        resultado = service.atualizar_quantidade(usuario_id=1, item_id=1, nova_quantidade=3)
        
        assert resultado is True
        mock_carrinho_repo.atualizar_quantidade_item.assert_called_once_with(1, 3)
    
    def test_atualizar_quantidade_zero_remove_item(self, service, mock_carrinho_repo, carrinho_valido):
        """Testa que quantidade zero remove o item."""
        item_existente = {'id': 1, 'produto_id': 1, 'quantidade': 2}
        mock_carrinho_repo.obter_ou_criar.return_value = carrinho_valido
        mock_carrinho_repo.listar_itens.return_value = [item_existente]
        mock_carrinho_repo.remover_item.return_value = True
        
        resultado = service.atualizar_quantidade(usuario_id=1, item_id=1, nova_quantidade=0)
        
        assert resultado is True
        mock_carrinho_repo.remover_item.assert_called_once_with(1)
    
    def test_atualizar_quantidade_negativa(self, service):
        """Testa atualização com quantidade negativa."""
        with pytest.raises(CarrinhoServiceError, match="não pode ser negativa"):
            service.atualizar_quantidade(usuario_id=1, item_id=1, nova_quantidade=-1)
    
    # Testes de calcular_total
    
    def test_calcular_total(self, service, mock_carrinho_repo, carrinho_valido):
        """Testa cálculo do total."""
        mock_carrinho_repo.obter_ou_criar.return_value = carrinho_valido
        mock_carrinho_repo.calcular_total.return_value = 5000.00
        
        total = service.calcular_total(usuario_id=1)
        
        assert total == Decimal('5000.00')
    
    # Testes de validar_carrinho_para_compra
    
    def test_validar_carrinho_vazio(self, service, mock_carrinho_repo, carrinho_valido):
        """Testa validação de carrinho vazio."""
        mock_carrinho_repo.obter_ou_criar.return_value = carrinho_valido
        mock_carrinho_repo.listar_itens.return_value = []
        
        with pytest.raises(CarrinhoServiceError, match="Carrinho está vazio"):
            service.validar_carrinho_para_compra(usuario_id=1)
    
    def test_validar_carrinho_produto_sem_estoque(self, service, mock_carrinho_repo, mock_produto_repo, carrinho_valido):
        """Testa validação com produto sem estoque."""
        itens = [{
            'id': 1,
            'produto_id': 1,
            'produto_nome': 'Notebook',
            'quantidade': 5,
            'preco_unitario': 2500.00
        }]
        produto_sem_estoque = {
            'id': 1,
            'nome': 'Notebook',
            'preco': 2500.00,
            'estoque': 2,
            'ativo': True
        }
        
        mock_carrinho_repo.obter_ou_criar.return_value = carrinho_valido
        mock_carrinho_repo.listar_itens.return_value = itens
        mock_produto_repo.buscar_por_id.return_value = produto_sem_estoque
        mock_carrinho_repo.calcular_total.return_value = 12500.00
        
        resultado = service.validar_carrinho_para_compra(usuario_id=1)
        
        assert resultado['valido'] is False
        assert len(resultado['erros']) > 0
        assert 'Estoque insuficiente' in resultado['erros'][0]
    
    def test_validar_carrinho_preco_alterado(self, service, mock_carrinho_repo, mock_produto_repo, carrinho_valido):
        """Testa validação com preço alterado."""
        itens = [{
            'id': 1,
            'produto_id': 1,
            'produto_nome': 'Notebook',
            'quantidade': 2,
            'preco_unitario': 2500.00
        }]
        produto_preco_novo = {
            'id': 1,
            'nome': 'Notebook',
            'preco': 2800.00,  # Preço aumentou
            'estoque': 10,
            'ativo': True
        }
        
        mock_carrinho_repo.obter_ou_criar.return_value = carrinho_valido
        mock_carrinho_repo.listar_itens.return_value = itens
        mock_produto_repo.buscar_por_id.return_value = produto_preco_novo
        mock_carrinho_repo.calcular_total.return_value = 5000.00
        
        resultado = service.validar_carrinho_para_compra(usuario_id=1)
        
        assert resultado['valido'] is True
        assert len(resultado['avisos']) > 0
        assert 'Preço' in resultado['avisos'][0]
    
    def test_validar_carrinho_valido(self, service, mock_carrinho_repo, mock_produto_repo, carrinho_valido, produto_valido):
        """Testa validação de carrinho válido."""
        itens = [{
            'id': 1,
            'produto_id': 1,
            'produto_nome': 'Notebook',
            'quantidade': 2,
            'preco_unitario': 2500.00
        }]
        
        mock_carrinho_repo.obter_ou_criar.return_value = carrinho_valido
        mock_carrinho_repo.listar_itens.return_value = itens
        mock_produto_repo.buscar_por_id.return_value = produto_valido
        mock_carrinho_repo.calcular_total.return_value = 5000.00
        
        resultado = service.validar_carrinho_para_compra(usuario_id=1)
        
        assert resultado['valido'] is True
        assert len(resultado['erros']) == 0
        assert resultado['total_itens'] == 1
        assert resultado['valor_total'] == 5000.00
    
    # Testes de limpar_carrinho
    
    def test_limpar_carrinho(self, service, mock_carrinho_repo, carrinho_valido):
        """Testa limpeza do carrinho."""
        mock_carrinho_repo.obter_ou_criar.return_value = carrinho_valido
        mock_carrinho_repo.limpar.return_value = True
        
        resultado = service.limpar_carrinho(usuario_id=1)
        
        assert resultado is True
        mock_carrinho_repo.limpar.assert_called_once_with(1)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
