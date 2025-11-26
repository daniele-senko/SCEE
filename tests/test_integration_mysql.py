#!/usr/bin/env python3
"""
Teste completo de integração MySQL com todos os repositories
"""
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

from config.database import get_connection, init_db
from repositories.usuario_repository import UsuarioRepository
from repositories.cliente_repository import ClienteRepository
from repositories.categoria_repository import CategoriaRepository
from repositories.produto_repository import ProdutoRepository
from repositories.carrinho_repository import CarrinhoRepository
from repositories.pedido_repository import PedidoRepository
import bcrypt


def test_connection():
    """Testa a conexão básica"""
    print("\n🔍 1. TESTANDO CONEXÃO...")
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"✅ MySQL conectado: {version['VERSION()']}")
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


def test_usuario_repository():
    """Testa UsuarioRepository"""
    print("\n📋 2. TESTANDO USUARIO REPOSITORY...")
    try:
        repo = UsuarioRepository(get_connection)
        
        # Buscar usuário existente (do seed)
        usuario = repo.buscar_por_email("admin@scee.com")
        if usuario:
            print(f"✅ Usuário encontrado: {usuario['nome']} ({usuario['email']})")
        else:
            print("⚠️  Usuário admin não encontrado no seed")
        
        # Listar usuários
        usuarios = repo.listar(limit=5)
        print(f"✅ Total de usuários listados: {len(usuarios)}")
        
        # Contar por tipo
        total_clientes = repo.contar_por_tipo('cliente')
        print(f"✅ Total de clientes: {total_clientes}")
        
        return True
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_categoria_repository():
    """Testa CategoriaRepository"""
    print("\n🏷️  3. TESTANDO CATEGORIA REPOSITORY...")
    try:
        repo = CategoriaRepository(get_connection)
        
        # Listar categorias
        categorias = repo.listar()
        print(f"✅ Total de categorias: {len(categorias)}")
        
        if categorias:
            print(f"   Primeira categoria: {categorias[0]['nome']}")
        
        # Listar apenas ativas
        ativas = repo.listar_ativas()
        print(f"✅ Categorias ativas: {len(ativas)}")
        
        return True
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_produto_repository():
    """Testa ProdutoRepository"""
    print("\n📦 4. TESTANDO PRODUTO REPOSITORY...")
    try:
        repo = ProdutoRepository(get_connection)
        
        # Listar produtos
        produtos = repo.listar(limit=5)
        print(f"✅ Total de produtos: {len(produtos)}")
        
        if produtos:
            prod = produtos[0]
            print(f"   Primeiro produto: {prod['nome']} - R$ {prod['preco']}")
            
            # Buscar por SKU
            produto_sku = repo.buscar_por_sku(prod['sku'])
            if produto_sku:
                print(f"✅ Produto encontrado por SKU: {produto_sku['nome']}")
        
        # Buscar com filtros
        resultado = repo.buscar_com_filtros(preco_max=200.00, limit=10)
        print(f"✅ Produtos até R$ 200: {len(resultado)}")
        
        return True
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_carrinho_repository():
    """Testa CarrinhoRepository"""
    print("\n🛒 5. TESTANDO CARRINHO REPOSITORY...")
    try:
        repo_carrinho = CarrinhoRepository(get_connection)
        repo_produto = ProdutoRepository(get_connection)
        repo_usuario = UsuarioRepository(get_connection)
        
        # Buscar um usuário cliente
        usuario = repo_usuario.buscar_por_email("joao@email.com")
        if not usuario:
            print("⚠️  Usuário de teste não encontrado")
            return False
        
        # Obter ou criar carrinho
        carrinho = repo_carrinho.obter_ou_criar(usuario['id'])
        print(f"✅ Carrinho obtido/criado: ID {carrinho['id']}")
        
        # Limpar carrinho (para teste limpo)
        repo_carrinho.limpar(carrinho['id'])
        print(f"✅ Carrinho limpo")
        
        # Listar produtos para adicionar
        produtos = repo_produto.listar(limit=2)
        if produtos:
            # Adicionar item ao carrinho
            item = repo_carrinho.adicionar_item(
                carrinho['id'],
                produtos[0]['id'],
                2,
                produtos[0]['preco']
            )
            print(f"✅ Item adicionado ao carrinho")
            
            # Listar itens
            itens = repo_carrinho.listar_itens(carrinho['id'])
            print(f"✅ Itens no carrinho: {len(itens)}")
            
            # Calcular total
            total = repo_carrinho.calcular_total(carrinho['id'])
            print(f"✅ Total do carrinho: R$ {total:.2f}")
        
        return True
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_pedido_repository():
    """Testa PedidoRepository"""
    print("\n📦 6. TESTANDO PEDIDO REPOSITORY...")
    try:
        repo = PedidoRepository(get_connection)
        
        # Listar pedidos
        pedidos = repo.listar(limit=5)
        print(f"✅ Total de pedidos: {len(pedidos)}")
        
        # Listar por status
        pendentes = repo.listar_por_status('PENDENTE')
        print(f"✅ Pedidos pendentes: {len(pendentes)}")
        
        return True
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Executa todos os testes"""
    print("=" * 70)
    print("🧪 TESTE COMPLETO DE INTEGRAÇÃO MYSQL - SCEE")
    print("=" * 70)
    
    resultados = []
    
    # Teste 1: Conexão
    resultados.append(("Conexão MySQL", test_connection()))
    
    # Teste 2-6: Repositories
    if resultados[0][1]:  # Só testa repositories se conexão OK
        resultados.append(("Usuario Repository", test_usuario_repository()))
        resultados.append(("Categoria Repository", test_categoria_repository()))
        resultados.append(("Produto Repository", test_produto_repository()))
        resultados.append(("Carrinho Repository", test_carrinho_repository()))
        resultados.append(("Pedido Repository", test_pedido_repository()))
    
    # Resumo
    print("\n" + "=" * 70)
    print("📊 RESUMO DOS TESTES")
    print("=" * 70)
    
    sucesso = 0
    falha = 0
    
    for nome, resultado in resultados:
        status = "✅ PASSOU" if resultado else "❌ FALHOU"
        print(f"{nome:.<50} {status}")
        if resultado:
            sucesso += 1
        else:
            falha += 1
    
    print(f"\n{'Total:':<50} {sucesso} passou, {falha} falhou")
    
    if falha == 0:
        print("\n🎉 TODOS OS TESTES PASSARAM! Sistema 100% funcional com MySQL!")
    else:
        print(f"\n⚠️  {falha} teste(s) falharam. Verifique os erros acima.")
    
    print("=" * 70)
    
    return falha == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
