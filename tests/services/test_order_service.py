"""Testes para o PedidoService."""
import pytest
from src.services.order_service import (
    PedidoService,
    PedidoServiceError,
    StatusInvalidoError,
    TransicaoStatusInvalidaError,
    PedidoNaoEncontradoError,
    CancelamentoNaoPermitidoError
)
from src.repositories.order_repository import PedidoRepository
from src.repositories.product_repository import ProductRepository
from src.repositories.user_repository import UsuarioRepository


class TestPedidoService:
    """Testes do serviço de pedidos."""
    
    def test_criar_pedido_sucesso(self, db_connection):
        """Testa criação de pedido."""
        pedido_repo = PedidoRepository()
        produto_repo = ProductRepository()
        usuario_repo = UsuarioRepository()
        service = PedidoService(pedido_repo, produto_repo, usuario_repo)
        
        # Criar pedido para cliente 2
        pedido = service.criar_pedido(
            usuario_id=2,
            endereco_id=1,
            itens=[
                {'produto_id': 1, 'quantidade': 2, 'preco_unitario': 199.90}
            ],
            tipo_pagamento='CARTAO',
            frete=15.00
        )
        
        assert pedido is not None
        assert pedido['usuario_id'] == 2
        assert pedido['status'] == 'PENDENTE'
        assert float(pedido['total']) > 0
    
    def test_criar_pedido_sem_itens(self, db_connection):
        """Testa erro ao criar pedido sem itens."""
        pedido_repo = PedidoRepository()
        produto_repo = ProductRepository()
        usuario_repo = UsuarioRepository()
        service = PedidoService(pedido_repo, produto_repo, usuario_repo)
        
        with pytest.raises(PedidoServiceError, match="pelo menos um item"):
            service.criar_pedido(
                usuario_id=2,
                endereco_id=1,
                itens=[],
                tipo_pagamento='CARTAO'
            )
    
    def test_criar_pedido_tipo_pagamento_invalido(self, db_connection):
        """Testa erro com tipo de pagamento inválido."""
        pedido_repo = PedidoRepository()
        produto_repo = ProductRepository()
        usuario_repo = UsuarioRepository()
        service = PedidoService(pedido_repo, produto_repo, usuario_repo)
        
        with pytest.raises(PedidoServiceError, match="Tipo de pagamento inválido"):
            service.criar_pedido(
                usuario_id=2,
                endereco_id=1,
                itens=[{'produto_id': 1, 'quantidade': 1, 'preco_unitario': 100.0}],
                tipo_pagamento='INVALIDO'
            )
    
    def test_buscar_por_id(self, db_connection):
        """Testa busca de pedido por ID."""
        pedido_repo = PedidoRepository()
        produto_repo = ProductRepository()
        usuario_repo = UsuarioRepository()
        service = PedidoService(pedido_repo, produto_repo, usuario_repo)
        
        # Criar pedido
        pedido = service.criar_pedido(
            usuario_id=2,
            endereco_id=1,
            itens=[{'produto_id': 1, 'quantidade': 1, 'preco_unitario': 199.90}],
            tipo_pagamento='PIX'
        )
        
        # Buscar
        pedido_buscado = service.buscar_por_id(pedido['id'])
        
        assert pedido_buscado is not None
        assert pedido_buscado['id'] == pedido['id']
    
    def test_atualizar_status_sucesso(self, db_connection):
        """Testa atualização de status de pedido."""
        pedido_repo = PedidoRepository()
        produto_repo = ProductRepository()
        usuario_repo = UsuarioRepository()
        service = PedidoService(pedido_repo, produto_repo, usuario_repo)
        
        # Criar pedido
        pedido = service.criar_pedido(
            usuario_id=2,
            endereco_id=1,
            itens=[{'produto_id': 1, 'quantidade': 1, 'preco_unitario': 199.90}],
            tipo_pagamento='BOLETO'
        )
        
        # Atualizar para PROCESSANDO (transição válida de PENDENTE)
        resultado = service.atualizar_status(pedido['id'], 'PROCESSANDO')
        
        assert resultado is True
        
        # Verificar status
        pedido_atualizado = service.buscar_por_id(pedido['id'])
        assert pedido_atualizado['status'] == 'PROCESSANDO'
    
    def test_atualizar_status_transicao_invalida(self, db_connection):
        """Testa erro em transição de status inválida."""
        pedido_repo = PedidoRepository()
        produto_repo = ProductRepository()
        usuario_repo = UsuarioRepository()
        service = PedidoService(pedido_repo, produto_repo, usuario_repo)
        
        # Criar pedido
        pedido = service.criar_pedido(
            usuario_id=2,
            endereco_id=1,
            itens=[{'produto_id': 1, 'quantidade': 1, 'preco_unitario': 199.90}],
            tipo_pagamento='CARTAO'
        )
        
        # Tentar transição inválida (PENDENTE -> ENTREGUE)
        with pytest.raises(TransicaoStatusInvalidaError):
            service.atualizar_status(pedido['id'], 'ENTREGUE')
    
    def test_cancelar_pedido_sucesso(self, db_connection):
        """Testa cancelamento de pedido."""
        pedido_repo = PedidoRepository()
        produto_repo = ProductRepository()
        usuario_repo = UsuarioRepository()
        service = PedidoService(pedido_repo, produto_repo, usuario_repo)
        
        # Criar pedido
        pedido = service.criar_pedido(
            usuario_id=2,
            endereco_id=1,
            itens=[{'produto_id': 1, 'quantidade': 1, 'preco_unitario': 199.90}],
            tipo_pagamento='PIX',
            observacoes="Pedido de teste"
        )
        
        # Cancelar
        resultado = service.cancelar_pedido(pedido['id'], usuario_id=2, motivo="Teste")
        
        assert resultado is True
        
        # Verificar status
        pedido_cancelado = service.buscar_por_id(pedido['id'])
        assert pedido_cancelado['status'] == 'CANCELADO'
    
    def test_listar_pedidos_por_status(self, db_connection):
        """Testa listagem de pedidos por status."""
        pedido_repo = PedidoRepository()
        produto_repo = ProductRepository()
        usuario_repo = UsuarioRepository()
        service = PedidoService(pedido_repo, produto_repo, usuario_repo)
        
        # Criar pedido PENDENTE
        service.criar_pedido(
            usuario_id=2,
            endereco_id=1,
            itens=[{'produto_id': 1, 'quantidade': 1, 'preco_unitario': 100.0}],
            tipo_pagamento='CARTAO'
        )
        
        # Listar pedidos PENDENTE
        pedidos = service.listar_pedidos_por_status('PENDENTE')
        
        assert len(pedidos) >= 1
        assert all(p['status'] == 'PENDENTE' for p in pedidos)
    
    def test_obter_estatisticas(self, db_connection):
        """Testa obtenção de estatísticas de pedidos."""
        pedido_repo = PedidoRepository()
        produto_repo = ProductRepository()
        usuario_repo = UsuarioRepository()
        service = PedidoService(pedido_repo, produto_repo, usuario_repo)
        
        # Criar pedido
        service.criar_pedido(
            usuario_id=2,
            endereco_id=1,
            itens=[{'produto_id': 1, 'quantidade': 1, 'preco_unitario': 199.90}],
            tipo_pagamento='CARTAO'
        )
        
        # Obter estatísticas
        stats = service.obter_estatisticas()
        
        assert 'total_pedidos' in stats
        assert 'por_status' in stats
        assert stats['total_pedidos'] >= 1
