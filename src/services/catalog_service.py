import os
import shutil
import uuid
from pathlib import Path
from typing import List, Optional

from src.models.products.product_model import Produto
from src.models.products.category_model import Categoria
from src.repositories.product_repository import ProductRepository
from src.repositories.category_repository import CategoriaRepository 
from src.config.settings import Config

class CatalogService:
    """
    Serviço responsável pelas Regras de Negócio do Catálogo e Gerenciamento de Arquivos.
    """

    def __init__(self):
        self.product_repo = ProductRepository()
        self.category_repo = CategoriaRepository()
        
        # Define pasta de uploads (cria se não existir)
        self.upload_dir = os.path.join(os.getcwd(), 'uploads', 'produtos')
        os.makedirs(self.upload_dir, exist_ok=True)

    def listar_categorias(self) -> List[Categoria]:
        """Busca categorias e converte para Objetos."""
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
        """Busca produtos, categorias e imagens."""
        # Agora o repositório já traz a imagem principal na view ou podemos buscar
        dados_produtos = self.product_repo.listar()
        
        categorias_objs = self.listar_categorias()
        mapa_categorias = {c.id: c for c in categorias_objs}
        
        lista_produtos = []
        for item in dados_produtos:
            # Garante que temos um dicionário
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
            # Se vier imagem da query (se você atualizou o listar do repo ou view)
            # prod.imagem_url = dado.get('imagem_principal') 
            
            lista_produtos.append(prod)
                
        return lista_produtos

    def cadastrar_produto(self, nome: str, sku: str, preco: float, estoque: int, 
                          nome_categoria: str, imagem_path: Optional[str] = None):
        """
        Cadastra produto e, se houver imagem, faz o upload.
        """
        # Valida Categoria
        categoria_selecionada = self._buscar_categoria_por_nome(nome_categoria)

        # Prepara Dict
        produto_dict = {
            'nome': nome,
            'sku': sku,
            'preco': float(preco),
            'estoque': int(estoque),
            'categoria_id': categoria_selecionada.id,
            'descricao': '',
            'ativo': 1
        }

        # Salva Produto (Recupera ID gerado)
        novo_produto = self.product_repo.salvar(produto_dict)
        produto_id = novo_produto['id']

        # Processa Imagem (Se fornecida)
        if imagem_path:
            caminho_final = self._salvar_arquivo_em_disco(imagem_path)
            self.product_repo.salvar_imagem(produto_id, caminho_final)

    def atualizar_produto(self, produto_id: int, nome: str, sku: str, preco: float, 
                          estoque: int, nome_categoria: str, imagem_path: Optional[str] = None):
        """
        Atualiza produto e adiciona nova imagem se fornecida.
        """
        categoria_selecionada = self._buscar_categoria_por_nome(nome_categoria)

        produto_dict = {
            'id': produto_id,
            'nome': nome,
            'sku': sku,
            'preco': float(preco),
            'estoque': int(estoque),
            'categoria_id': categoria_selecionada.id,
            'descricao': '',
            'ativo': 1
        }

        self.product_repo.atualizar(produto_dict)

        # Se houver nova imagem, salvamos (Adicionando à galeria do produto)
        if imagem_path:
            caminho_final = self._salvar_arquivo_em_disco(imagem_path)
            self.product_repo.salvar_imagem(produto_id, caminho_final)

    def remover_produto(self, id_produto: int):
        # Nota: Idealmente deletaríamos os arquivos de imagem do disco aqui também
        return self.product_repo.deletar(id_produto)

    # --- MÉTODOS AUXILIARES ---

    def _buscar_categoria_por_nome(self, nome: str) -> Categoria:
        categorias = self.listar_categorias()
        categoria = next((c for c in categorias if c.nome == nome), None)
        if not categoria:
            raise ValueError(f"Categoria '{nome}' inválida.")
        return categoria

    def _salvar_arquivo_em_disco(self, caminho_origem: str) -> str:
        """
        Copia o arquivo para a pasta do sistema e retorna o caminho relativo.
        """
        if not os.path.exists(caminho_origem):
            raise FileNotFoundError("Arquivo de imagem não encontrado.")

        # Gera nome único para evitar colisão (ex: produto_uuid.jpg)
        extensao = os.path.splitext(caminho_origem)[1]
        nome_arquivo = f"{uuid.uuid4()}{extensao}"
        caminho_destino = os.path.join(self.upload_dir, nome_arquivo)

        # Copia o arquivo
        shutil.copy2(caminho_origem, caminho_destino)

        # Retorna o caminho relativo para salvar no banco (melhor para portabilidade)
        return os.path.join('uploads', 'produtos', nome_arquivo)