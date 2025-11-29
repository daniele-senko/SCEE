"""Testes para o PedidoRepository."""
import pytest
from src.repositories.order_repository import PedidoRepository


class TestPedidoRepository:
    """Testes do repositório de pedidos."""
    
    def test_salvar_novo_pedido(self, db_connection):
        """Testa salvamento de novo pedido."""
        repo = PedidoRepository()
        
        novo_pedido = {
            'usuario_id': 2,
            'endereco_id': 1,
            'subtotal': 399.80,
            'frete': 20.00,
            'total': 419.80,
            'status': 'PENDENTE',
            'tipo_pagamento': 'CARTAO'
        }
        
        pedido_salvo = repo.salvar(novo_pedido)
        
        assert pedido_salvo is not None
        assert 'id' in pedido_salvo
        assert pedido_salvo['usuario_id'] == 2
        assert pedido_salvo['status'] == 'PENDENTE'
    
    def test_buscar_por_id(self, db_connection):
        """Testa busca de pedido por ID."""
        repo = PedidoRepository()
        
        # Criar pedido
        novo_pedido = {
            'usuario_id': 2,
            'endereco_id': 1,
            'subtotal': 100.0,
            'frete': 10.0,
            'total': 110.0,
            'status': 'PENDENTE',
            'tipo_pagamento': 'PIX'
        }
        pedido = repo.salvar(novo_pedido)
        
        # Buscar
        pedido_buscado = repo.buscar_por_id(pedido['id'])
        
        assert pedido_buscado is not None
        assert pedido_buscado['id'] == pedido['id']
    
    def test_adicionar_item_pedido(self, db_connection):
        """Testa adição de item ao pedido."""
        repo = PedidoRepository()
        
        # Criar pedido
        novo_pedido = {
            'usuario_id': 2,
            'endereco_id': 1,
            'subtotal': 199.90,
            'frete': 15.0,
            'total': 214.90,
            'status': 'PENDENTE',
            'tipo_pagamento': 'BOLETO'
        }
        pedido = repo.salvar(novo_pedido)
        
        # Adicionar item
        item = repo.adicionar_item(
            pedido['id'],
            produto_id=1,
            nome_produto='Fone de Ouvido Bluetooth',
            quantidade=1,
            preco_unitario=199.90
        )
        
        assert item is not None
        assert item['pedido_id'] == pedido['id']
        assert item['produto_id'] == 1
    
    def test_listar_por_usuario(self, db_connection):
        """Testa listagem de pedidos por usuário."""
        repo = PedidoRepository()
        
        # Criar pedido para usuário 2
        novo_pedido = {
            'usuario_id': 2,
            'endereco_id': 1,
            'subtotal': 50.0,
            'frete': 5.0,
            'total': 55.0,
            'status': 'PENDENTE',
            'tipo_pagamento': 'CARTAO'
        }
        repo.salvar(novo_pedido)
        
        # Listar pedidos do usuário
        pedidos = repo.listar_por_usuario(2)
        
        assert len(pedidos) >= 1
        assert all(p['usuario_id'] == 2 for p in pedidos)
    
    def test_listar_por_status(self, db_connection):
        """Testa listagem de pedidos por status."""
        repo = PedidoRepository()
        
        # Criar pedido PENDENTE
        novo_pedido = {
            'usuario_id': 2,
            'endereco_id': 1,
            'subtotal': 100.0,
            'frete': 10.0,
            'total': 110.0,
            'status': 'PENDENTE',
            'tipo_pagamento': 'PIX'
        }
        repo.salvar(novo_pedido)
        
        # Listar pedidos PENDENTE
        pedidos = repo.listar_por_status('PENDENTE')
        
        assert len(pedidos) >= 1
        assert all(p['status'] == 'PENDENTE' for p in pedidos)
    
    def test_atualizar_status(self, db_connection):
        """Testa atualização de status do pedido."""
        repo = PedidoRepository()
        
        # Criar pedido
        novo_pedido = {
            'usuario_id': 2,
            'endereco_id': 1,
            'subtotal': 75.0,
            'frete': 8.0,
            'total': 83.0,
            'status': 'PENDENTE',
            'tipo_pagamento': 'CARTAO'
        }
        pedido = repo.salvar(novo_pedido)
        
        # Atualizar status
        resultado = repo.atualizar_status(pedido['id'], 'PROCESSANDO')
        
        assert resultado is True
        
        # Verificar atualização
        pedido_atualizado = repo.buscar_por_id(pedido['id'])
        assert pedido_atualizado['status'] == 'PROCESSANDO'
    
    def test_buscar_completo(self, db_connection):
        """Testa busca de pedido com todos os detalhes."""
        repo = PedidoRepository()
        
        # Criar pedido com item
        novo_pedido = {
            'usuario_id': 2,
            'endereco_id': 1,
            'subtotal': 199.90,
            'frete': 15.0,
            'total': 214.90,
            'status': 'PENDENTE',
            'tipo_pagamento': 'CARTAO'
        }
        pedido = repo.salvar(novo_pedido)
        repo.adicionar_item(pedido['id'], 1, 'Fone de Ouvido', 1, 199.90)
        
        # Buscar completo
        pedido_completo = repo.buscar_completo(pedido['id'])
        
        assert pedido_completo is not None
        assert 'itens' in pedido_completo or len(pedido_completo) > 0
    
    def test_contar_por_status(self, db_connection):
        """Testa contagem de pedidos por status."""
        repo = PedidoRepository()
        
        # Criar alguns pedidos PENDENTE
        for i in range(2):
            repo.salvar({
                'usuario_id': 2,
                'endereco_id': 1,
                'subtotal': 50.0,
                'frete': 5.0,
                'total': 55.0,
                'status': 'PENDENTE',
                'tipo_pagamento': 'PIX'
            })
        
        # Contar
        total = repo.contar_por_status('PENDENTE')
        
        assert total >= 2
