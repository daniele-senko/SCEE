"""Testes para o EnderecoRepository."""
import pytest
from src.repositories.address_repository import EnderecoRepository


class TestEnderecoRepository:
    """Testes do repositório de endereços."""
    
    def test_salvar_novo_endereco(self, db_connection):
        """Testa salvamento de novo endereço."""
        repo = EnderecoRepository()
        
        novo_endereco = {
            'usuario_id': 2,
            'logradouro': 'Rua Teste',
            'numero': '100',
            'complemento': 'Apto 10',
            'bairro': 'Centro',
            'cidade': 'São Paulo',
            'estado': 'SP',
            'cep': '01000-000',
            'principal': 0
        }
        
        endereco_salvo = repo.salvar(novo_endereco)
        
        assert endereco_salvo is not None
        assert 'id' in endereco_salvo
        assert endereco_salvo['logradouro'] == 'Rua Teste'
        assert endereco_salvo['usuario_id'] == 2
    
    def test_buscar_por_id(self, db_connection):
        """Testa busca de endereço por ID."""
        repo = EnderecoRepository()
        
        # Criar endereço
        novo_endereco = {
            'usuario_id': 2,
            'logradouro': 'Av Principal',
            'numero': '200',
            'bairro': 'Jardim',
            'cidade': 'Rio de Janeiro',
            'estado': 'RJ',
            'cep': '20000-000',
            'principal': 0
        }
        endereco = repo.salvar(novo_endereco)
        
        # Buscar
        endereco_buscado = repo.buscar_por_id(endereco['id'])
        
        assert endereco_buscado is not None
        assert endereco_buscado['id'] == endereco['id']
        assert endereco_buscado['logradouro'] == 'Av Principal'
    
    def test_listar_por_usuario(self, db_connection):
        """Testa listagem de endereços por usuário."""
        repo = EnderecoRepository()
        
        # Criar endereços para usuário 2
        for i in range(2):
            repo.salvar({
                'usuario_id': 2,
                'logradouro': f'Rua {i}',
                'numero': f'{i}00',
                'bairro': 'Bairro',
                'cidade': 'Cidade',
                'estado': 'SP',
                'cep': '12345-678',
                'principal': 0
            })
        
        # Listar endereços
        enderecos = repo.listar_por_usuario(2)
        
        assert len(enderecos) >= 2
        assert all(e['usuario_id'] == 2 for e in enderecos)
    
    def test_atualizar_endereco(self, db_connection):
        """Testa atualização de endereço."""
        repo = EnderecoRepository()
        
        # Criar endereço
        novo_endereco = {
            'usuario_id': 2,
            'logradouro': 'Rua Original',
            'numero': '50',
            'bairro': 'Bairro',
            'cidade': 'Cidade',
            'estado': 'MG',
            'cep': '30000-000',
            'principal': 0
        }
        endereco = repo.salvar(novo_endereco)
        
        # Atualizar
        endereco['logradouro'] = 'Rua Atualizada'
        resultado = repo.atualizar(endereco)
        
        assert resultado is not None
        
        # Verificar atualização
        endereco_atualizado = repo.buscar_por_id(endereco['id'])
        assert endereco_atualizado['logradouro'] == 'Rua Atualizada'
    
    def test_deletar_endereco(self, db_connection):
        """Testa exclusão de endereço."""
        repo = EnderecoRepository()
        
        # Criar endereço
        novo_endereco = {
            'usuario_id': 2,
            'logradouro': 'Rua Para Deletar',
            'numero': '999',
            'bairro': 'Teste',
            'cidade': 'Teste',
            'estado': 'SP',
            'cep': '99999-999',
            'principal': 0
        }
        endereco = repo.salvar(novo_endereco)
        
        # Deletar
        resultado = repo.deletar(endereco['id'])
        
        assert resultado is True
        
        # Verificar que foi deletado
        endereco_deletado = repo.buscar_por_id(endereco['id'])
        assert endereco_deletado is None
    
    def test_definir_principal(self, db_connection):
        """Testa definição de endereço principal."""
        repo = EnderecoRepository()
        
        # Criar endereço
        novo_endereco = {
            'usuario_id': 2,
            'logradouro': 'Rua Principal',
            'numero': '1',
            'bairro': 'Centro',
            'cidade': 'São Paulo',
            'estado': 'SP',
            'cep': '01000-000',
            'principal': 0
        }
        endereco = repo.salvar(novo_endereco)
        
        # Definir como principal
        resultado = repo.definir_principal(endereco['id'], 2)
        
        assert resultado is True
        
        # Verificar que está principal
        endereco_atualizado = repo.buscar_por_id(endereco['id'])
        assert endereco_atualizado['principal'] == 1
    
    def test_buscar_principal(self, db_connection):
        """Testa busca de endereço principal."""
        repo = EnderecoRepository()
        
        # Criar e definir endereço principal
        novo_endereco = {
            'usuario_id': 2,
            'logradouro': 'Rua Principal',
            'numero': '1',
            'bairro': 'Centro',
            'cidade': 'São Paulo',
            'estado': 'SP',
            'cep': '01000-000',
            'principal': 0
        }
        endereco = repo.salvar(novo_endereco)
        repo.definir_principal(endereco['id'], 2)
        
        # Buscar principal
        endereco_principal = repo.buscar_principal(2)
        
        assert endereco_principal is not None
        assert endereco_principal['principal'] == 1
        assert endereco_principal['usuario_id'] == 2
