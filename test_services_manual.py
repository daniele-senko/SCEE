"""Script simples para testar manualmente os Services.

Este script demonstra como usar cada service com dados reais do banco.
Execute após garantir que o banco de dados está populado.

Uso:
    python test_services_manual.py
"""
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

from config.database import get_connection
from repositories.carrinho_repository import CarrinhoRepository
from repositories.produto_repository import ProdutoRepository
from repositories.pedido_repository import PedidoRepository
from repositories.usuario_repository import UsuarioRepository
from repositories.categoria_repository import CategoriaRepository
from src.services.carrinho_service import CarrinhoService
from src.services.pedido_service import PedidoService
from src.services.catalogo_service import CatalogoService
from src.services.usuario_service import UsuarioService
from src.services.email_service import EmailService, TipoEmail


def print_separator(title):
    """Imprime um separador visual."""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)


def test_carrinho_service():
    """Testa o CarrinhoService."""
    print_separator("TESTANDO CARRINHO SERVICE")
    
    carrinho_repo = CarrinhoRepository(get_connection)
    produto_repo = ProdutoRepository(get_connection)
    service = CarrinhoService(carrinho_repo, produto_repo)
    
    try:
        # 1. Adicionar item ao carrinho
        print("\n1️⃣  Adicionando item ao carrinho...")
        item = service.adicionar_item(
            usuario_id=1,
            produto_id=1,
            quantidade=2
        )
        print(f"✅ Item adicionado: {item}")
        
        # 2. Listar itens
        print("\n2️⃣  Listando itens do carrinho...")
        itens = service.listar_itens(usuario_id=1)
        print(f"📦 Total de itens: {len(itens)}")
        for item in itens:
            print(f"   - {item['produto_nome']}: {item['quantidade']}x R$ {item['preco_unitario']:.2f}")
        
        # 3. Calcular total
        print("\n3️⃣  Calculando total...")
        total = service.calcular_total(usuario_id=1)
        print(f"💰 Total: R$ {total:.2f}")
        
        # 4. Validar carrinho
        print("\n4️⃣  Validando carrinho para compra...")
        validacao = service.validar_carrinho_para_compra(usuario_id=1)
        print(f"✓ Válido: {validacao['valido']}")
        if validacao['erros']:
            print(f"❌ Erros: {validacao['erros']}")
        if validacao['avisos']:
            print(f"⚠️  Avisos: {validacao['avisos']}")
        
        # 5. Limpar carrinho
        print("\n5️⃣  Limpando carrinho...")
        service.limpar_carrinho(usuario_id=1)
        print("✅ Carrinho limpo")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()


def test_pedido_service():
    """Testa o PedidoService."""
    print_separator("TESTANDO PEDIDO SERVICE")
    
    pedido_repo = PedidoRepository(get_connection)
    produto_repo = ProdutoRepository(get_connection)
    usuario_repo = UsuarioRepository(get_connection)
    service = PedidoService(pedido_repo, produto_repo, usuario_repo)
    
    try:
        # 1. Criar pedido
        print("\n1️⃣  Criando pedido...")
        pedido = service.criar_pedido(
            usuario_id=1,
            endereco_id=1,
            itens=[
                {'produto_id': 1, 'quantidade': 1, 'preco_unitario': 2500.00}
            ],
            tipo_pagamento='CARTAO',
            frete=15.00
        )
        print(f"✅ Pedido criado: #{pedido['id']}")
        print(f"   Status: {pedido['status']}")
        print(f"   Total: R$ {pedido['total']:.2f}")
        
        # 2. Buscar pedido completo
        print("\n2️⃣  Buscando pedido completo...")
        pedido_completo = service.buscar_por_id(pedido['id'], completo=True)
        print(f"📦 Pedido #{pedido_completo['id']}")
        print(f"   Itens: {len(pedido_completo['itens'])}")
        
        # 3. Atualizar status
        print("\n3️⃣  Atualizando status...")
        service.atualizar_status(pedido['id'], 'PROCESSANDO')
        print("✅ Status atualizado para PROCESSANDO")
        
        # 4. Obter histórico completo
        print("\n4️⃣  Obtendo histórico completo...")
        historico = service.obter_historico_completo(pedido['id'])
        print(f"📋 Status atual: {historico['status']}")
        print(f"   Pode cancelar: {historico['pode_cancelar']}")
        print(f"   Próximos status: {historico['proximos_status']}")
        
        # 5. Obter estatísticas
        print("\n5️⃣  Obtendo estatísticas...")
        stats = service.obter_estatisticas()
        print(f"📊 Total de pedidos: {stats['total_pedidos']}")
        print(f"   Por status: {stats['por_status']}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()


def test_catalogo_service():
    """Testa o CatalogoService."""
    print_separator("TESTANDO CATÁLOGO SERVICE")
    
    produto_repo = ProdutoRepository(get_connection)
    categoria_repo = CategoriaRepository(get_connection)
    service = CatalogoService(produto_repo, categoria_repo)
    
    try:
        # 1. Listar categorias
        print("\n1️⃣  Listando categorias...")
        categorias = service.listar_categorias()
        print(f"📁 Total de categorias: {len(categorias)}")
        for cat in categorias[:3]:
            print(f"   - {cat['nome']}: {cat['total_produtos']} produtos")
        
        # 2. Buscar produtos
        print("\n2️⃣  Buscando produtos...")
        resultado = service.buscar_produtos(
            pagina=1,
            itens_por_pagina=5
        )
        print(f"🔍 Encontrados {len(resultado['produtos'])} produtos")
        for prod in resultado['produtos'][:3]:
            print(f"   - {prod['nome']}: R$ {prod['preco']:.2f} (estoque: {prod['estoque']})")
        
        # 3. Produtos em destaque
        print("\n3️⃣  Produtos em destaque...")
        destaques = service.obter_destaques(limite=3)
        print(f"⭐ {len(destaques)} produtos em destaque")
        for prod in destaques:
            print(f"   - {prod['nome']}: R$ {prod['preco']:.2f}")
        
        # 4. Faixa de preços
        print("\n4️⃣  Faixa de preços do catálogo...")
        faixa = service.obter_faixa_precos()
        print(f"💰 Mín: R$ {faixa['min']:.2f} | Máx: R$ {faixa['max']:.2f}")
        
        # 5. Validar disponibilidade
        print("\n5️⃣  Validando disponibilidade de produto...")
        disp = service.validar_disponibilidade(produto_id=1, quantidade=2)
        print(f"✓ Disponível: {disp['disponivel']}")
        if not disp['disponivel']:
            print(f"   Motivo: {disp['motivo']}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()


def test_usuario_service():
    """Testa o UsuarioService."""
    print_separator("TESTANDO USUÁRIO SERVICE")
    
    usuario_repo = UsuarioRepository(get_connection)
    service = UsuarioService(usuario_repo)
    
    try:
        # 1. Buscar usuário
        print("\n1️⃣  Buscando usuário...")
        usuario = service.buscar_por_id(1)
        print(f"👤 Usuário: {usuario['nome']}")
        print(f"   Email: {usuario['email']}")
        print(f"   Tipo: {usuario['tipo']}")
        
        # 2. Obter estatísticas
        print("\n2️⃣  Obtendo estatísticas...")
        stats = service.obter_estatisticas()
        print(f"📊 Total de usuários: {stats['total_usuarios']}")
        print(f"   Clientes: {stats['total_clientes']}")
        print(f"   Administradores: {stats['total_administradores']}")
        
        # 3. Verificar se é admin
        print("\n3️⃣  Verificando permissões...")
        eh_admin = service.eh_admin(1)
        print(f"🔐 Usuário #1 é admin: {eh_admin}")
        
        # 4. Listar usuários
        print("\n4️⃣  Listando usuários...")
        usuarios = service.listar_usuarios(limit=5)
        print(f"👥 Total: {len(usuarios)}")
        for u in usuarios[:3]:
            print(f"   - {u['nome']} ({u['tipo']})")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()


def test_email_service():
    """Testa o EmailService."""
    print_separator("TESTANDO EMAIL SERVICE")
    
    service = EmailService(modo_mock=True)
    
    try:
        # 1. Enviar email simples
        print("\n1️⃣  Enviando email simples...")
        sucesso = service.enviar_email(
            destinatario='cliente@teste.com',
            assunto='Teste',
            corpo='Este é um email de teste'
        )
        print(f"✅ Email enviado: {sucesso}")
        
        # 2. Enviar email com template
        print("\n2️⃣  Enviando email com template...")
        sucesso = service.enviar_email_template(
            destinatario='cliente@teste.com',
            tipo=TipoEmail.BEM_VINDO,
            dados={'nome': 'João Silva'}
        )
        print(f"✅ Email template enviado: {sucesso}")
        
        # 3. Adicionar à fila
        print("\n3️⃣  Adicionando email à fila...")
        email_id = service.adicionar_a_fila(
            destinatario='cliente@teste.com',
            assunto='Email em fila',
            corpo='Este email está na fila',
            prioridade=3
        )
        print(f"📬 Email adicionado à fila: {email_id}")
        
        # 4. Processar fila
        print("\n4️⃣  Processando fila de emails...")
        resultado = service.processar_fila()
        print(f"✅ Processados: {resultado['processados']}")
        print(f"   Sucessos: {resultado['sucessos']}")
        print(f"   Falhas: {resultado['falhas']}")
        
        # 5. Histórico
        print("\n5️⃣  Obtendo histórico...")
        historico = service.obter_historico(limite=3)
        print(f"📋 Emails no histórico: {len(historico)}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Executa todos os testes."""
    print("\n" + "🧪 " * 20)
    print("  TESTE MANUAL DOS SERVICES - SCEE")
    print("🧪 " * 20)
    
    print("\n⚠️  IMPORTANTE: Certifique-se de que o banco está populado!")
    print("   Execute: python warmup_database.py")
    
    input("\n▶️  Pressione ENTER para continuar...")
    
    # Executar testes
    test_carrinho_service()
    test_pedido_service()
    test_catalogo_service()
    test_usuario_service()
    test_email_service()
    
    print("\n" + "="*60)
    print("  ✅ TODOS OS TESTES CONCLUÍDOS!")
    print("="*60)


if __name__ == '__main__':
    main()
