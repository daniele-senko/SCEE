"""Testes para o CategoriaRepository."""
import pytest
from src.repositories.category_repository import CategoriaRepository


class TestCategoriaRepository:
    """Testes do repositório de categorias."""
    
    def test_buscar_por_id(self, db_connection):
        """Testa busca de categoria por ID."""
        repo = CategoriaRepository()
        
        # Categoria ID 1 existe no seeder (Eletrônicos)
        categoria = repo.buscar_por_id(1)
        
        assert categoria is not None
        assert categoria['id'] == 1
        assert categoria['nome'] == 'Eletrônicos'
    
    def test_buscar_por_id_inexistente(self, db_connection):
        """Testa busca de categoria inexistente."""
        repo = CategoriaRepository()
        
        categoria = repo.buscar_por_id(99999)
        
        assert categoria is None
    
    def test_listar_categorias(self, db_connection):
        """Testa listagem de categorias."""
        repo = CategoriaRepository()
        
        categorias = repo.listar()
        
        assert len(categorias) >= 5  # Seeder adiciona 5 categorias
        assert all('nome' in c for c in categorias)
        # Verifica categorias do seeder
        nomes = [c['nome'] for c in categorias]
        assert 'Eletrônicos' in nomes
        assert 'Roupas' in nomes
        assert 'Livros' in nomes
    
    def test_salvar_nova_categoria(self, db_connection):
        """Testa salvamento de nova categoria."""
        repo = CategoriaRepository()
        
        nova_categoria = {
            'nome': 'Categoria Teste',
            'descricao': 'Descrição da categoria teste',
            'ativo': 1
        }
        
        categoria_salva = repo.salvar(nova_categoria)
        
        assert categoria_salva is not None
        assert 'id' in categoria_salva
        assert categoria_salva['nome'] == 'Categoria Teste'
    
    def test_atualizar_categoria(self, db_connection):
        """Testa atualização de categoria."""
        repo = CategoriaRepository()
        
        # Buscar categoria existente
        categoria = repo.buscar_por_id(1)
        categoria['descricao'] = 'Nova descrição de eletrônicos'
        
        # Atualizar
        resultado = repo.atualizar(categoria)
        
        assert resultado is not None
        
        # Verificar atualização
        categoria_atualizada = repo.buscar_por_id(1)
        assert categoria_atualizada['descricao'] == 'Nova descrição de eletrônicos'
    
    def test_deletar_categoria(self, db_connection):
        """Testa exclusão de categoria."""
        repo = CategoriaRepository()
        
        # Criar categoria para deletar
        nova_categoria = {
            'nome': 'Categoria Para Deletar',
            'descricao': 'Teste',
            'ativo': 1
        }
        categoria = repo.salvar(nova_categoria)
        
        # Deletar
        resultado = repo.deletar(categoria['id'])
        
        assert resultado is True
        
        # Verificar que foi deletada
        categoria_deletada = repo.buscar_por_id(categoria['id'])
        assert categoria_deletada is None
    
    def test_buscar_por_nome(self, db_connection):
        """Testa busca de categoria por nome."""
        repo = CategoriaRepository()
        
        categoria = repo.buscar_por_nome('Eletrônicos')
        
        assert categoria is not None
        assert categoria['nome'] == 'Eletrônicos'
        assert categoria['id'] == 1
