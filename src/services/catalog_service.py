import os
import shutil
import uuid
from typing import List, Optional, Dict, Any

from src.models.products.product_model import Produto
from src.models.products.category_model import Categoria
from src.repositories.product_repository import ProductRepository
from src.repositories.category_repository import CategoryRepository 
from src.config.settings import Config

class CatalogService:
    """
    Serviço responsável pelas Regras de Negócio do Catálogo.
    """

    def __init__(self):
        self.product_repo = ProductRepository()
        self.category_repo = CategoryRepository()
        
        self.upload_dir = os.path.join(Config.BASE_DIR, 'uploads', 'produtos')
        os.makedirs(self.upload_dir, exist_ok=True)

    def listar_categorias(self) -> List[Categoria]:
        dados_brutos = self.category_repo.listar()
        lista_objetos = []
        for item in dados_brutos:
            if isinstance(item, dict):
                cat = Categoria(nome=item['nome'], id=item['id'])
                lista_objetos.append(cat)
            else:
                lista_objetos.append(item)
        return lista_objetos

    def listar_produtos(self) -> List[Produto]:
        dados_produtos = self.product_repo.listar()
        
        categorias_objs = self.listar_categorias()
        mapa_categorias = {c.id: c for c in categorias_objs}
        
        lista_produtos = []
        for item in dados_produtos:
            dado = item if isinstance(item, dict) else item.__dict__
            
            cat_id = dado.get('categoria_id')
            categoria = mapa_categorias.get(cat_id)
            
            prod = Produto(
                nome=dado['nome'],
                sku=dado['sku'],
                preco=float(dado['preco']),
                estoque=int(dado.get('estoque', 0)),
                categoria=categoria,
                id=dado['id']
            )
            
            # Preenche campos extras do objeto
            if 'descricao' in dado:
                prod.descricao = dado['descricao']
            if 'imagem_principal' in dado:
                prod.imagem_principal = dado['imagem_principal']
            if 'imagens' in dado:
                prod.imagens = dado['imagens']
            if 'ativo' in dado:
                prod.ativo = dado['ativo']
            
            lista_produtos.append(prod)
                
        return lista_produtos

    def cadastrar_produto(self, nome: str, sku: str, preco: float, estoque: int, 
                          nome_categoria: str, descricao: str = "", imagem_path: Optional[str] = None):
        
        categoria_selecionada = self._buscar_categoria_por_nome(nome_categoria)

        produto_dict = {
            'nome': nome,
            'sku': sku,
            'preco': float(preco),
            'estoque': int(estoque),
            'categoria_id': categoria_selecionada.id,
            'descricao': descricao,
            'ativo': 1
        }

        novo_produto = self.product_repo.salvar(produto_dict)
        produto_id = novo_produto['id']

        if imagem_path:
            caminho_final = self._salvar_arquivo_em_disco(imagem_path)
            self.product_repo.salvar_imagem(produto_id, caminho_final)

    def atualizar_produto(self, produto_id: int, nome: str, sku: str, preco: float, 
                          estoque: int, nome_categoria: str, descricao: str = "", imagem_path: Optional[str] = None):
        
        categoria_selecionada = self._buscar_categoria_por_nome(nome_categoria)

        produto_dict = {
            'id': produto_id,
            'nome': nome,
            'sku': sku,
            'preco': float(preco),
            'estoque': int(estoque),
            'categoria_id': categoria_selecionada.id,
            'descricao': descricao,
            'ativo': 1
        }

        self.product_repo.atualizar(produto_dict)

        if imagem_path:
            caminho_final = self._salvar_arquivo_em_disco(imagem_path)
            self.product_repo.salvar_imagem(produto_id, caminho_final)

    def remover_produto(self, id_produto: int):
        return self.product_repo.deletar(id_produto)

    # --- Métodos Privados ---

    def _buscar_categoria_por_nome(self, nome: str) -> Categoria:
        categorias = self.listar_categorias()
        categoria = next((c for c in categorias if c.nome == nome), None)
        if not categoria:
            raise ValueError(f"Categoria '{nome}' inválida.")
        return categoria

    def _salvar_arquivo_em_disco(self, caminho_origem: str) -> str:
        if not os.path.exists(caminho_origem):
            raise FileNotFoundError("Arquivo de imagem não encontrado.")

        extensao = os.path.splitext(caminho_origem)[1]
        nome_arquivo = f"{uuid.uuid4()}{extensao}"
        caminho_destino = os.path.join(self.upload_dir, nome_arquivo)

        shutil.copy2(caminho_origem, caminho_destino)
        return os.path.join('uploads', 'produtos', nome_arquivo)