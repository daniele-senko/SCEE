"""Testes para o ProductRepository."""
import pytest
from src.repositories.product_repository import ProductRepository


class TestProductRepository:
    """Testes do repositório de produtos."""
    
    def test_buscar_por_id(self, db_connection):
        """Testa busca de produto por ID."""
        repo = ProductRepository()
        
        # Produto ID 1 existe no seeder (Fone de Ouvido)
        produto = repo.buscar_por_id(1)
        
        assert produto is not None
        assert produto['id'] == 1
        assert produto['nome'] == 'Fone de Ouvido Bluetooth'
        assert produto['preco'] == 199.90
    
    def test_buscar_por_id_inexistente(self, db_connection):
        """Testa busca de produto inexistente."""
        repo = ProductRepository()
        
        produto = repo.buscar_por_id(99999)
        
        assert produto is None
    
    def test_listar_produtos(self, db_connection):
        """Testa listagem de produtos."""
        repo = ProductRepository()
        
        produtos = repo.listar()
        
        assert len(produtos) >= 15  # Seeder adiciona 15 produtos
        assert all('nome' in p for p in produtos)
        assert all('preco' in p for p in produtos)
    
    def test_listar_produtos_com_categoria(self, db_connection):
        """Testa listagem de produtos (inclui nome da categoria)."""
        repo = ProductRepository()
        
        produtos = repo.listar()
        
        # Verifica se produtos têm categoria_nome (JOIN feito no listar)
        assert len(produtos) >= 15
        assert any('categoria_nome' in p for p in produtos)
    
    def test_salvar_novo_produto(self, db_connection):
        """Testa salvamento de novo produto."""
        repo = ProductRepository()
        
        novo_produto = {
            'nome': 'Produto Teste',
            'descricao': 'Descrição do produto teste',
            'preco': 99.90,
            'sku': 'TEST-001',
            'categoria_id': 1,
            'estoque': 10,
            'ativo': 1
        }
        
        produto_salvo = repo.salvar(novo_produto)
        
        assert produto_salvo is not None
        assert 'id' in produto_salvo
        assert produto_salvo['nome'] == 'Produto Teste'
    
    def test_atualizar_produto(self, db_connection):
        """Testa atualização de produto."""
        repo = ProductRepository()
        
        # Buscar produto existente
        produto = repo.buscar_por_id(1)
        produto['preco'] = 249.90
        
        # Atualizar
        resultado = repo.atualizar(produto)
        
        assert resultado is not None
        
        # Verificar atualização
        produto_atualizado = repo.buscar_por_id(1)
        assert produto_atualizado['preco'] == 249.90
    
    def test_deletar_produto(self, db_connection):
        """Testa exclusão de produto."""
        repo = ProductRepository()
        
        # Criar produto para deletar
        novo_produto = {
            'nome': 'Produto Para Deletar',
            'descricao': 'Teste',
            'preco': 50.0,
            'sku': 'DEL-001',
            'categoria_id': 1,
            'estoque': 5,
            'ativo': 1
        }
        produto = repo.salvar(novo_produto)
        
        # Deletar
        resultado = repo.deletar(produto['id'])
        
        assert resultado is True
        
        # Verificar que foi deletado
        produto_deletado = repo.buscar_por_id(produto['id'])
        assert produto_deletado is None
    
    def test_deletar_produto_inexistente(self, db_connection):
        """Testa exclusão de produto inexistente."""
        repo = ProductRepository()
        
        resultado = repo.deletar(99999)
        
        assert resultado is False
