"""Repositório para gerenciamento de produtos e suas imagens."""
from typing import Optional, List, Dict, Any, Union
from src.repositories.base_repository import BaseRepository
from src.models.products.product_model import Produto

class ProductRepository(BaseRepository[Dict[str, Any]]):
    """Repositório de produtos com operações CRUD e gerenciamento de imagens."""
    
    def __init__(self):
        super().__init__()

    def _adaptar_para_dict(self, obj: Union[Produto, Dict]) -> Dict:
        """Helper para converter Objeto Produto em Dicionário."""
        if isinstance(obj, dict):
            return obj
        
        return {
            "id": getattr(obj, "id", None),
            "nome": getattr(obj, "nome", ""),
            "sku": getattr(obj, "sku", ""),
            "preco": getattr(obj, "preco", 0.0),
            "estoque": getattr(obj, "estoque", 0),
            "categoria_id": obj.categoria.id if obj.categoria else None,
            "descricao": getattr(obj, "descricao", ""),
            "ativo": 1
        }

    def salvar(self, obj_entrada: Union[Produto, Dict]) -> Dict[str, Any]:
        """Salva um novo produto e retorna o dicionário com ID."""
        obj = self._adaptar_para_dict(obj_entrada)

        query = """
            INSERT INTO produtos 
            (nome, descricao, preco, sku, categoria_id, estoque, ativo)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(
                query,
                (
                    obj['nome'],
                    obj.get('descricao'),
                    obj['preco'],
                    obj['sku'],
                    obj.get('categoria_id'),
                    obj.get('estoque', 0),
                    obj.get('ativo', 1)
                )
            )
            conn.commit()
            obj['id'] = cursor.lastrowid
            
            # Atualiza ID do objeto original se for objeto
            if hasattr(obj_entrada, '_id'):
                obj_entrada._id = cursor.lastrowid
        
        return obj

    def salvar_imagem(self, produto_id: int, caminho_imagem: str, prioridade: int = 0):
        """Salva o caminho/URL de uma imagem vinculada ao produto."""
        query = """
            INSERT INTO imagens_produto (produto_id, url, prioridade)
            VALUES (?, ?, ?)
        """
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (produto_id, caminho_imagem, prioridade))
            conn.commit()

    def buscar_imagens(self, produto_id: int) -> List[str]:
        """Retorna lista de URLs/Caminhos das imagens do produto."""
        query = "SELECT url FROM imagens_produto WHERE produto_id = ? ORDER BY prioridade"
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (produto_id,))
            rows = cursor.fetchall()
            return [row[0] for row in rows]
    
    def buscar_por_id(self, id: int) -> Optional[Dict[str, Any]]:
        """Busca um produto por ID, incluindo suas imagens."""
        query = "SELECT * FROM produtos WHERE id = ?"
        
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (id,))
            row = cursor.fetchone()
            
            if row:
                dados = dict(row)
                # Agora buscamos as imagens para retornar o produto completo
                dados['imagens'] = self.buscar_imagens(id)
                return dados
            return None
    
    def listar(self, limit: Optional[int] = None, offset: int = 0) -> List[Dict[str, Any]]:
        """Lista produtos com JOIN na categoria."""
        query = """
            SELECT p.*, c.nome as categoria_nome 
            FROM produtos p
            LEFT JOIN categorias c ON p.categoria_id = c.id
            ORDER BY p.nome
        """
        
        params = []
        if limit is not None:
            query += " LIMIT ? OFFSET ?"
            params.extend([limit, offset])
        
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, tuple(params))
            rows = cursor.fetchall()
            # Na listagem geral, optamos por não carregar as imagens de todos 
            # para manter a performance (Lazy Loading), ou carregamos apenas a principal se necessário.
            return [dict(row) for row in rows]
    
    def atualizar(self, obj_entrada: Union[Produto, Dict]) -> Dict[str, Any]:
        """Atualiza um produto."""
        obj = self._adaptar_para_dict(obj_entrada)

        if 'id' not in obj or not obj['id']:
            raise ValueError("Produto deve ter um ID para ser atualizado")
        
        query = """
            UPDATE produtos
            SET nome = ?, descricao = ?, preco = ?, sku = ?,
                categoria_id = ?, estoque = ?, ativo = ?
            WHERE id = ?
        """
        
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(
                query,
                (
                    obj['nome'],
                    obj.get('descricao'),
                    obj['preco'],
                    obj['sku'],
                    obj.get('categoria_id'),
                    obj.get('estoque', 0),
                    obj.get('ativo', 1),
                    obj['id']
                )
            )
            conn.commit()
        
        return obj
    
    def deletar(self, id: int) -> bool:
        """Deleta um produto por ID."""
        # O banco já tem ON DELETE CASCADE, então as imagens somem do DB automaticamente.
        query = "DELETE FROM produtos WHERE id = ?"
        
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (id,))
            conn.commit()
            return cursor.rowcount > 0