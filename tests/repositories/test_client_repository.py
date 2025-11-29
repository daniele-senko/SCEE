"""Testes para o ClienteRepository."""
import pytest
from src.repositories.client_repository import ClienteRepository


class TestClienteRepository:
    """Testes do repositório de clientes."""
    
    def test_buscar_por_usuario_id(self, db_connection):
        """Testa busca de cliente por usuario_id."""
        repo = ClienteRepository()
        
        # Usuario ID 2 é cliente (João Silva)
        cliente = repo.buscar_por_usuario_id(2)
        
        assert cliente is not None
        assert cliente['usuario_id'] == 2
        assert 'cpf' in cliente
    
    def test_buscar_por_id_inexistente(self, db_connection):
        """Testa busca de cliente inexistente."""
        repo = ClienteRepository()
        
        cliente = repo.buscar_por_id(99999)
        
        assert cliente is None
    
    def test_buscar_completo(self, db_connection):
        """Testa busca completa de cliente (com dados do usuário)."""
        repo = ClienteRepository()
        
        # Usuario ID 2 é cliente
        cliente = repo.buscar_completo(2)
        
        assert cliente is not None
        assert cliente['email'] == 'joao@email.com'
        assert cliente['nome'] == 'João Silva'
        assert 'cpf' in cliente
    
    def test_buscar_por_cpf(self, db_connection):
        """Testa busca de cliente por CPF."""
        repo = ClienteRepository()
        
        # CPF do cliente do seeder
        cliente = repo.buscar_por_cpf('123.456.789-00')
        
        assert cliente is not None
        assert cliente['cpf'] == '123.456.789-00'
    
    def test_listar_clientes(self, db_connection):
        """Testa listagem de clientes."""
        repo = ClienteRepository()
        
        clientes = repo.listar()
        
        assert len(clientes) >= 1  # Pelo menos o cliente do seeder
        assert all('cpf' in c for c in clientes)
        assert all('usuario_id' in c for c in clientes)
    
    def test_atualizar_cliente(self, db_connection):
        """Testa atualização de cliente."""
        repo = ClienteRepository()
        
        # Buscar cliente existente
        cliente = repo.buscar_por_usuario_id(2)
        cliente['telefone'] = '(11) 99999-9999'
        
        # Atualizar
        resultado = repo.atualizar(cliente)
        
        assert resultado is not None
        
        # Verificar atualização
        cliente_atualizado = repo.buscar_por_usuario_id(2)
        assert cliente_atualizado['telefone'] == '(11) 99999-9999'
    
    def test_salvar_novo_cliente(self, db_connection):
        """Testa salvamento de novo cliente."""
        repo = ClienteRepository()
        
        # Usuario ID 1 é admin, não tem cliente_info
        novo_cliente = {
            'usuario_id': 1,
            'cpf': '999.999.999-99',
            'telefone': '(11) 98888-8888'
        }
        
        cliente_salvo = repo.salvar(novo_cliente)
        
        assert cliente_salvo is not None
        assert 'id' in cliente_salvo
        assert cliente_salvo['cpf'] == '999.999.999-99'
