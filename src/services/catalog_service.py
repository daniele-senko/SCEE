from typing import List, Optional
from src.models.products.product_model import Produto
from src.models.products.category_model import Categoria
from src.repositories.product_repository import ProductRepository
# CORREÇÃO 1: Importamos o nome em Português (como está no arquivo do seu amigo)
from src.repositories.category_repository import CategoriaRepository 

class CatalogService:
    """
    Serviço responsável pelas Regras de Negócio do Catálogo.
    Atua como ADAPTADOR entre os Repositórios (que retornam Dicts do MySQL)
    e as Views (que esperam Objetos Python).
    """

    def __init__(self):
        self.product_repo = ProductRepository()
        # CORREÇÃO 2: Instanciamos a classe com o nome correto
        self.category_repo = CategoriaRepository()

    def listar_categorias(self) -> List[Categoria]:
        """
        Busca categorias no banco (Dict) e converte para Objetos (Categoria).
        """
        dados_brutos = self.category_repo.listar()
        lista_objetos = []
        
        for item in dados_brutos:
            # Verifica se veio dicionário e converte
            if isinstance(item, dict):
                cat = Categoria(nome=item['nome'], id=item['id'])
                lista_objetos.append(cat)
            else:
                # Se já for objeto (caso mude no futuro)
                lista_objetos.append(item)
                
        return lista_objetos

    def listar_produtos(self) -> List[Produto]:
        """
        Busca produtos no banco (Dict) e converte para Objetos (Produto).
        Também preenche a Categoria de cada produto.
        """
        dados_produtos = self.product_repo.listar()
        
        # Otimização: Busca todas as categorias para poder vincular pelo ID
        categorias_objs = self.listar_categorias()
        mapa_categorias = {c.id: c for c in categorias_objs}
        
        lista_produtos = []
        for item in dados_produtos:
            if isinstance(item, dict):
                # Pega o objeto categoria correspondente ao ID
                cat_id = item.get('categoria_id')
                categoria = mapa_categorias.get(cat_id)
                
                # Cria o objeto Produto
                prod = Produto(
                    nome=item['nome'],
                    sku=item['sku'],
                    preco=float(item['preco']),
                    estoque=int(item.get('estoque', 0)),
                    categoria=categoria, # Pode ser None se não achar
                    id=item['id']
                )
                lista_produtos.append(prod)
            else:
                lista_produtos.append(item)
                
        return lista_produtos

    def cadastrar_produto(self, nome: str, sku: str, preco: float, estoque: int, nome_categoria: str):
        """
        Recebe dados da tela, valida e salva no repositório.
        """
        # 1. Busca a categoria pelo nome (vindo do Combobox da tela)
        categorias = self.listar_categorias()
        categoria_selecionada = next((c for c in categorias if c.nome == nome_categoria), None)
        
        if not categoria_selecionada:
            raise ValueError(f"Categoria '{nome_categoria}' inválida.")

        # 2. Prepara o Dicionário para o Repositório do seu amigo
        # (O repo dele espera um Dict, não um Objeto)
        produto_dict = {
            'nome': nome,
            'sku': sku,
            'preco': float(preco),
            'estoque': int(estoque),
            'categoria_id': categoria_selecionada.id,
            'descricao': '', # Campo obrigatório no banco dele
            'ativo': 1       # Campo obrigatório no banco dele
        }

        # 3. Salva
        self.product_repo.salvar(produto_dict)

    def atualizar_produto(self, produto_id: int, nome: str, sku: str, preco: float, estoque: int, nome_categoria: str):
        """
        Atualiza um produto existente.
        """
        # 1. Busca a categoria pelo nome
        categorias = self.listar_categorias()
        categoria_selecionada = next((c for c in categorias if c.nome == nome_categoria), None)
        
        if not categoria_selecionada:
            raise ValueError(f"Categoria '{nome_categoria}' inválida.")

        # 2. Prepara o Dicionário para atualização
        produto_dict = {
            'id': produto_id,
            'nome': nome,
            'sku': sku,
            'preco': float(preco),
            'estoque': int(estoque),
            'categoria_id': categoria_selecionada.id,
            'descricao': '',  # Mantém vazio se não for editável
            'ativo': 1
        }

        # 3. Atualiza
        self.product_repo.atualizar(produto_dict)

    def remover_produto(self, id_produto: int):
        return self.product_repo.deletar(id_produto)