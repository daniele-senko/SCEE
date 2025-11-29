"""Testes para o CarrinhoRepository."""
import pytest
from src.repositories.cart_repository import CarrinhoRepository


class TestCarrinhoRepository:
    """Testes do repositório de carrinho."""
    
    def test_obter_ou_criar_carrinho(self, db_connection):
        """Testa obtenção ou criação de carrinho."""
        repo = CarrinhoRepository()
        
        # Cliente ID 2 existe no seeder
        carrinho = repo.obter_ou_criar(2)
        
        assert carrinho is not None
        assert carrinho['usuario_id'] == 2
        assert 'id' in carrinho
    
    def test_obter_carrinho_existente(self, db_connection):
        """Testa obtenção de carrinho já existente."""
        repo = CarrinhoRepository()
        
        # Criar carrinho
        carrinho1 = repo.obter_ou_criar(2)
        
        # Obter novamente (deve retornar o mesmo)
        carrinho2 = repo.obter_ou_criar(2)
        
        assert carrinho1['id'] == carrinho2['id']
    
    def test_adicionar_item(self, db_connection):
        """Testa adição de item ao carrinho."""
        repo = CarrinhoRepository()
        
        # Obter carrinho
        carrinho = repo.obter_ou_criar(2)
        
        # Adicionar item (Produto 1 - Fone de Ouvido - R$ 199.90)
        item = repo.adicionar_item(
            carrinho['id'],
            produto_id=1,
            quantidade=2,
            preco_unitario=199.90
        )
        
        assert item is not None
        assert item['produto_id'] == 1
        assert item['quantidade'] == 2
        assert item['preco_unitario'] == 199.90
    
    def test_listar_itens(self, db_connection):
        """Testa listagem de itens do carrinho."""
        repo = CarrinhoRepository()
        
        # Obter carrinho e adicionar item
        carrinho = repo.obter_ou_criar(2)
        repo.adicionar_item(carrinho['id'], 1, 2, 199.90)
        
        # Listar itens
        itens = repo.listar_itens(carrinho['id'])
        
        assert len(itens) >= 1
        assert any(item['produto_id'] == 1 for item in itens)
    
    def test_calcular_total(self, db_connection):
        """Testa cálculo do total do carrinho."""
        repo = CarrinhoRepository()
        
        # Obter carrinho e adicionar itens
        carrinho = repo.obter_ou_criar(2)
        repo.adicionar_item(carrinho['id'], 1, 2, 199.90)  # 2 x 199.90 = 399.80
        
        # Calcular total
        total = repo.calcular_total(carrinho['id'])
        
        assert total > 0
        assert total >= 399.80
    
    def test_atualizar_quantidade_item(self, db_connection):
        """Testa atualização de quantidade de item."""
        repo = CarrinhoRepository()
        
        # Obter carrinho e adicionar item
        carrinho = repo.obter_ou_criar(2)
        item = repo.adicionar_item(carrinho['id'], 1, 2, 199.90)
        
        # Atualizar quantidade
        resultado = repo.atualizar_quantidade_item(item['id'], 5)
        
        assert resultado is True
        
        # Verificar atualização
        itens = repo.listar_itens(carrinho['id'])
        item_atualizado = next(i for i in itens if i['id'] == item['id'])
        assert item_atualizado['quantidade'] == 5
    
    def test_remover_item(self, db_connection):
        """Testa remoção de item do carrinho."""
        repo = CarrinhoRepository()
        
        # Obter carrinho e adicionar item
        carrinho = repo.obter_ou_criar(2)
        item = repo.adicionar_item(carrinho['id'], 1, 1, 199.90)
        
        # Remover item
        resultado = repo.remover_item(item['id'])
        
        assert resultado is True
        
        # Verificar remoção
        itens = repo.listar_itens(carrinho['id'])
        assert not any(i['id'] == item['id'] for i in itens)
    
    def test_limpar_carrinho(self, db_connection):
        """Testa limpeza de todos os itens do carrinho."""
        repo = CarrinhoRepository()
        
        # Obter carrinho e adicionar itens
        carrinho = repo.obter_ou_criar(2)
        repo.adicionar_item(carrinho['id'], 1, 1, 199.90)
        repo.adicionar_item(carrinho['id'], 2, 2, 129.90)
        
        # Limpar carrinho
        resultado = repo.limpar(carrinho['id'])
        
        assert resultado is True
        
        # Verificar que está vazio
        itens = repo.listar_itens(carrinho['id'])
        assert len(itens) == 0
