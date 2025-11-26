#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Aquecimento do Banco de Dados

Testa todos os repositories criando, lendo, atualizando e deletando registros.
Útil para validar a conexão e performance do banco de dados.
"""

import sys
import logging
from datetime import datetime
from decimal import Decimal

from config.database import get_connection
from repositories.usuario_repository import UsuarioRepository
from repositories.categoria_repository import CategoriaRepository
from repositories.produto_repository import ProdutoRepository
from repositories.cliente_repository import ClienteRepository
from repositories.endereco_repository import EnderecoRepository
from repositories.carrinho_repository import CarrinhoRepository
from repositories.pedido_repository import PedidoRepository

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DatabaseWarmup:
    """Classe para aquecimento do banco de dados"""
    
    def __init__(self):
        """Inicializa os repositories"""
        self.usuario_repo = UsuarioRepository(get_connection)
        self.categoria_repo = CategoriaRepository(get_connection)
        self.produto_repo = ProdutoRepository(get_connection)
        self.cliente_repo = ClienteRepository(get_connection)
        self.endereco_repo = EnderecoRepository(get_connection)
        self.carrinho_repo = CarrinhoRepository(get_connection)
        self.pedido_repo = PedidoRepository(get_connection)
        
        # Armazenar IDs criados para limpeza
        self.created_ids = {
            'usuarios': [],
            'categorias': [],
            'produtos': [],
            'clientes': [],
            'enderecos': [],
            'carrinhos': [],
            'pedidos': []
        }
    
    def run(self):
        """Executa o aquecimento completo do banco"""
        logger.info("=" * 80)
        logger.info("INICIANDO AQUECIMENTO DO BANCO DE DADOS")
        logger.info("=" * 80)
        
        try:
            # Teste de cada repository
            self.test_usuario_repository()
            self.test_categoria_repository()
            self.test_produto_repository()
            self.test_cliente_repository()
            self.test_endereco_repository()
            self.test_carrinho_repository()
            self.test_pedido_repository()
            
            logger.info("\n" + "=" * 80)
            logger.info("✅ AQUECIMENTO CONCLUÍDO COM SUCESSO!")
            logger.info("=" * 80)
            
        except Exception as e:
            logger.error(f"\n❌ ERRO DURANTE AQUECIMENTO: {e}", exc_info=True)
            raise
        finally:
            # Limpar dados de teste
            self.cleanup()
    
    def test_usuario_repository(self):
        """Testa UsuarioRepository"""
        logger.info("\n" + "-" * 80)
        logger.info("🔄 Testando UsuarioRepository")
        logger.info("-" * 80)
        
        # CREATE
        usuario = {
            'nome': 'Teste Warmup',
            'email': f'warmup_{datetime.now().timestamp()}@teste.com',
            'senha_hash': 'senha_hash_123',
            'tipo': 'cliente'
        }
        logger.info(f"📝 Criando usuário: {usuario['email']}")
        usuario_criado = self.usuario_repo.salvar(usuario)
        self.created_ids['usuarios'].append(usuario_criado['id'])
        logger.info(f"✅ Usuário criado com ID: {usuario_criado['id']}")
        
        # READ
        logger.info(f"🔍 Buscando usuário por ID: {usuario_criado['id']}")
        usuario_lido = self.usuario_repo.buscar_por_id(usuario_criado['id'])
        assert usuario_lido is not None, "Usuário não encontrado"
        logger.info(f"✅ Usuário encontrado: {usuario_lido['nome']}")
        
        # READ BY EMAIL
        logger.info(f"🔍 Buscando usuário por email: {usuario['email']}")
        usuario_email = self.usuario_repo.buscar_por_email(usuario['email'])
        assert usuario_email is not None, "Usuário não encontrado por email"
        logger.info(f"✅ Usuário encontrado por email")
        
        # UPDATE
        usuario_criado['nome'] = 'Teste Warmup Atualizado'
        logger.info(f"📝 Atualizando usuário: {usuario_criado['nome']}")
        usuario_atualizado = self.usuario_repo.atualizar(usuario_criado)
        logger.info(f"✅ Usuário atualizado")
        
        # LIST
        logger.info("📋 Listando usuários (limit 5)")
        usuarios = self.usuario_repo.listar(limit=5)
        logger.info(f"✅ {len(usuarios)} usuários listados")
    
    def test_categoria_repository(self):
        """Testa CategoriaRepository"""
        logger.info("\n" + "-" * 80)
        logger.info("🔄 Testando CategoriaRepository")
        logger.info("-" * 80)
        
        # CREATE
        categoria = {
            'nome': f'Categoria Warmup {datetime.now().timestamp()}',
            'descricao': 'Categoria de teste para aquecimento'
        }
        logger.info(f"📝 Criando categoria: {categoria['nome']}")
        categoria_criada = self.categoria_repo.salvar(categoria)
        self.created_ids['categorias'].append(categoria_criada['id'])
        logger.info(f"✅ Categoria criada com ID: {categoria_criada['id']}")
        
        # READ
        logger.info(f"🔍 Buscando categoria por ID: {categoria_criada['id']}")
        categoria_lida = self.categoria_repo.buscar_por_id(categoria_criada['id'])
        assert categoria_lida is not None, "Categoria não encontrada"
        logger.info(f"✅ Categoria encontrada: {categoria_lida['nome']}")
        
        # UPDATE
        categoria_criada['nome'] = 'Categoria Warmup Atualizada'
        logger.info(f"📝 Atualizando categoria: {categoria_criada['nome']}")
        categoria_atualizada = self.categoria_repo.atualizar(categoria_criada)
        logger.info(f"✅ Categoria atualizada")
        
        # LIST
        logger.info("📋 Listando categorias")
        categorias = self.categoria_repo.listar()
        logger.info(f"✅ {len(categorias)} categorias listadas")
    
    def test_produto_repository(self):
        """Testa ProdutoRepository"""
        logger.info("\n" + "-" * 80)
        logger.info("🔄 Testando ProdutoRepository")
        logger.info("-" * 80)
        
        # Precisa de uma categoria
        if not self.created_ids['categorias']:
            logger.warning("⚠️ Nenhuma categoria criada, pulando teste de produto")
            return
        
        categoria_id = self.created_ids['categorias'][0]
        
        # CREATE
        produto = {
            'nome': f'Produto Warmup {datetime.now().timestamp()}',
            'descricao': 'Produto de teste para aquecimento',
            'preco': Decimal('99.99'),
            'estoque': 100,
            'categoria_id': categoria_id,
            'sku': f'WARM-{int(datetime.now().timestamp())}',
            'ativo': True
        }
        logger.info(f"📝 Criando produto: {produto['nome']}")
        produto_criado = self.produto_repo.salvar(produto)
        self.created_ids['produtos'].append(produto_criado['id'])
        logger.info(f"✅ Produto criado com ID: {produto_criado['id']}")
        
        # READ
        logger.info(f"🔍 Buscando produto por ID: {produto_criado['id']}")
        produto_lido = self.produto_repo.buscar_por_id(produto_criado['id'])
        assert produto_lido is not None, "Produto não encontrado"
        logger.info(f"✅ Produto encontrado: {produto_lido['nome']}")
        
        # READ BY SKU
        logger.info(f"🔍 Buscando produto por SKU: {produto['sku']}")
        produto_sku = self.produto_repo.buscar_por_sku(produto['sku'])
        assert produto_sku is not None, "Produto não encontrado por SKU"
        logger.info(f"✅ Produto encontrado por SKU")
        
        # UPDATE
        produto_criado['preco'] = Decimal('89.99')
        produto_criado['estoque'] = 90
        logger.info(f"📝 Atualizando produto: preço={produto_criado['preco']}, estoque={produto_criado['estoque']}")
        produto_atualizado = self.produto_repo.atualizar(produto_criado)
        logger.info(f"✅ Produto atualizado")
        
        # LIST
        logger.info("📋 Listando produtos (limit 5)")
        produtos = self.produto_repo.listar(limit=5)
        logger.info(f"✅ {len(produtos)} produtos listados")
        
        # SEARCH WITH FILTERS
        logger.info("🔍 Buscando produtos com filtros (busca='Warmup')")
        produtos_busca = self.produto_repo.buscar_com_filtros(busca='Warmup')
        logger.info(f"✅ {len(produtos_busca)} produtos encontrados na busca")
    
    def test_cliente_repository(self):
        """Testa ClienteRepository"""
        logger.info("\n" + "-" * 80)
        logger.info("🔄 Testando ClienteRepository")
        logger.info("-" * 80)
        
        # Precisa de um usuário
        if not self.created_ids['usuarios']:
            logger.warning("⚠️ Nenhum usuário criado, pulando teste de cliente")
            return
        
        usuario_id = self.created_ids['usuarios'][0]
        
        # CREATE
        cliente = {
            'usuario_id': usuario_id,
            'cpf': '12345678901',
            'telefone': '11999999999',
            'data_nascimento': '1990-01-01'
        }
        logger.info(f"📝 Criando cliente para usuário ID: {usuario_id}")
        cliente_criado = self.cliente_repo.salvar(cliente)
        self.created_ids['clientes'].append(cliente_criado['id'])
        logger.info(f"✅ Cliente criado com ID: {cliente_criado['id']}")
        
        # READ
        logger.info(f"🔍 Buscando cliente por ID: {cliente_criado['id']}")
        cliente_lido = self.cliente_repo.buscar_por_id(cliente_criado['id'])
        assert cliente_lido is not None, "Cliente não encontrado"
        logger.info(f"✅ Cliente encontrado")
        
        # READ BY USUARIO
        logger.info(f"🔍 Buscando cliente por usuário ID: {usuario_id}")
        cliente_usuario = self.cliente_repo.buscar_por_usuario_id(usuario_id)
        assert cliente_usuario is not None, "Cliente não encontrado por usuário"
        logger.info(f"✅ Cliente encontrado por usuário")
        
        # UPDATE
        cliente_criado['telefone'] = '11988888888'
        logger.info(f"📝 Atualizando cliente: telefone={cliente_criado['telefone']}")
        cliente_atualizado = self.cliente_repo.atualizar(cliente_criado)
        logger.info(f"✅ Cliente atualizado")
    
    def test_endereco_repository(self):
        """Testa EnderecoRepository"""
        logger.info("\n" + "-" * 80)
        logger.info("🔄 Testando EnderecoRepository")
        logger.info("-" * 80)
        
        # Precisa de um usuário (não cliente)
        if not self.created_ids['usuarios']:
            logger.warning("⚠️ Nenhum usuário criado, pulando teste de endereço")
            return
        
        usuario_id = self.created_ids['usuarios'][0]
        
        # CREATE
        endereco = {
            'usuario_id': usuario_id,
            'cep': '12345678',
            'logradouro': 'Rua Teste',
            'numero': '123',
            'complemento': 'Apto 45',
            'bairro': 'Centro',
            'cidade': 'São Paulo',
            'estado': 'SP',
            'principal': True
        }
        logger.info(f"📝 Criando endereço para usuário ID: {usuario_id}")
        endereco_criado = self.endereco_repo.salvar(endereco)
        self.created_ids['enderecos'].append(endereco_criado['id'])
        logger.info(f"✅ Endereço criado com ID: {endereco_criado['id']}")
        
        # READ
        logger.info(f"🔍 Buscando endereço por ID: {endereco_criado['id']}")
        endereco_lido = self.endereco_repo.buscar_por_id(endereco_criado['id'])
        assert endereco_lido is not None, "Endereço não encontrado"
        logger.info(f"✅ Endereço encontrado")
        
        # LIST BY USUARIO
        logger.info(f"📋 Listando endereços do usuário ID: {usuario_id}")
        enderecos = self.endereco_repo.listar_por_usuario(usuario_id)
        logger.info(f"✅ {len(enderecos)} endereços listados")
        
        # UPDATE
        endereco_criado['numero'] = '456'
        logger.info(f"📝 Atualizando endereço: numero={endereco_criado['numero']}")
        endereco_atualizado = self.endereco_repo.atualizar(endereco_criado)
        logger.info(f"✅ Endereço atualizado")
    
    def test_carrinho_repository(self):
        """Testa CarrinhoRepository"""
        logger.info("\n" + "-" * 80)
        logger.info("🔄 Testando CarrinhoRepository")
        logger.info("-" * 80)
        
        # Precisa de um usuário e produto
        if not self.created_ids['usuarios'] or not self.created_ids['produtos']:
            logger.warning("⚠️ Faltam usuário ou produto, pulando teste de carrinho")
            return
        
        usuario_id = self.created_ids['usuarios'][0]
        produto_id = self.created_ids['produtos'][0]
        
        # CREATE
        logger.info(f"📝 Criando carrinho para usuário ID: {usuario_id}")
        carrinho = self.carrinho_repo.obter_ou_criar(usuario_id)
        self.created_ids['carrinhos'].append(carrinho['id'])
        logger.info(f"✅ Carrinho criado/obtido com ID: {carrinho['id']}")
        
        # ADD ITEM
        logger.info(f"➕ Adicionando produto ID {produto_id} ao carrinho")
        item = self.carrinho_repo.adicionar_item(
            carrinho_id=carrinho['id'],
            produto_id=produto_id,
            quantidade=2,
            preco_unitario=99.99
        )
        logger.info(f"✅ Item adicionado ao carrinho")
        
        # LIST ITEMS
        logger.info(f"📋 Listando itens do carrinho ID: {carrinho['id']}")
        itens = self.carrinho_repo.listar_itens(carrinho['id'])
        logger.info(f"✅ {len(itens)} itens no carrinho")
        
        # CALCULATE TOTAL
        logger.info(f"💰 Calculando total do carrinho")
        total = self.carrinho_repo.calcular_total(carrinho['id'])
        logger.info(f"✅ Total do carrinho: R$ {total:.2f}")
        
        # UPDATE QUANTITY
        if itens:
            item_id = itens[0]['id']
            logger.info(f"📝 Atualizando quantidade do item ID {item_id} para 5")
            self.carrinho_repo.atualizar_quantidade_item(item_id, 5)
            logger.info(f"✅ Quantidade atualizada")
            
            # REMOVE ITEM
            logger.info(f"🗑️ Removendo item ID {item_id}")
            self.carrinho_repo.remover_item(item_id)
            logger.info(f"✅ Item removido")
        
        # CLEAR
        logger.info(f"🧹 Limpando carrinho")
        self.carrinho_repo.limpar(carrinho['id'])
        logger.info(f"✅ Carrinho limpo")
    
    def test_pedido_repository(self):
        """Testa PedidoRepository"""
        logger.info("\n" + "-" * 80)
        logger.info("🔄 Testando PedidoRepository")
        logger.info("-" * 80)
        
        # Precisa de usuário, endereço e produto
        if not self.created_ids['usuarios'] or not self.created_ids['enderecos'] or not self.created_ids['produtos']:
            logger.warning("⚠️ Faltam dados necessários, pulando teste de pedido")
            return
        
        usuario_id = self.created_ids['usuarios'][0]
        endereco_id = self.created_ids['enderecos'][0]
        produto_id = self.created_ids['produtos'][0]
        
        # CREATE
        pedido = {
            'usuario_id': usuario_id,
            'endereco_id': endereco_id,
            'subtotal': Decimal('199.98'),
            'frete': Decimal('15.00'),
            'total': Decimal('214.98'),
            'status': 'PENDENTE',
            'tipo_pagamento': 'CARTAO'  # Valores aceitos: CARTAO, PIX, BOLETO
        }
        logger.info(f"📝 Criando pedido para usuário ID: {usuario_id}")
        pedido_criado = self.pedido_repo.salvar(pedido)
        self.created_ids['pedidos'].append(pedido_criado['id'])
        logger.info(f"✅ Pedido criado com ID: {pedido_criado['id']}")
        
        # ADD ITEM
        logger.info(f"➕ Adicionando item ao pedido")
        item = self.pedido_repo.adicionar_item(
            pedido_id=pedido_criado['id'],
            produto_id=produto_id,
            nome_produto='Produto Warmup Teste',
            quantidade=2,
            preco_unitario=Decimal('99.99')
        )
        logger.info(f"✅ Item adicionado ao pedido")
        
        # READ
        logger.info(f"🔍 Buscando pedido por ID: {pedido_criado['id']}")
        pedido_lido = self.pedido_repo.buscar_por_id(pedido_criado['id'])
        assert pedido_lido is not None, "Pedido não encontrado"
        logger.info(f"✅ Pedido encontrado")
        
        # LIST ITEMS
        logger.info(f"📋 Listando itens do pedido")
        itens = self.pedido_repo.listar_itens(pedido_criado['id'])
        logger.info(f"✅ {len(itens)} itens no pedido")
        
        # UPDATE STATUS
        logger.info(f"📝 Atualizando status do pedido para PROCESSANDO")
        self.pedido_repo.atualizar_status(pedido_criado['id'], 'PROCESSANDO')
        logger.info(f"✅ Status atualizado")
        
        # LIST BY USUARIO
        logger.info(f"📋 Listando pedidos do usuário")
        pedidos = self.pedido_repo.listar_por_usuario(usuario_id)
        logger.info(f"✅ {len(pedidos)} pedidos do usuário")
    
    def cleanup(self):
        """Remove todos os dados de teste criados"""
        logger.info("\n" + "=" * 80)
        logger.info("🧹 LIMPANDO DADOS DE TESTE")
        logger.info("=" * 80)
        
        # Ordem de deleção respeitando foreign keys
        ordem_delecao = [
            ('pedidos', self.pedido_repo),
            ('carrinhos', self.carrinho_repo),
            ('enderecos', self.endereco_repo),
            ('produtos', self.produto_repo),
            ('clientes', self.cliente_repo),
            ('categorias', self.categoria_repo),
            ('usuarios', self.usuario_repo)
        ]
        
        for tabela, repo in ordem_delecao:
            ids = self.created_ids[tabela]
            if ids:
                logger.info(f"🗑️ Removendo {len(ids)} registro(s) de {tabela}")
                for id_item in ids:
                    try:
                        repo.deletar(id_item)
                        logger.info(f"  ✅ {tabela} ID {id_item} removido")
                    except Exception as e:
                        logger.warning(f"  ⚠️ Erro ao remover {tabela} ID {id_item}: {e}")
        
        logger.info("✅ Limpeza concluída")


def main():
    """Função principal"""
    try:
        warmup = DatabaseWarmup()
        warmup.run()
        return 0
    except Exception as e:
        logger.error(f"Erro fatal: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
