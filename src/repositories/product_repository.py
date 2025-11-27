"""Repositório para gerenciamento de produtos.
Implementa operações CRUD para a tabela produtos.
"""
from typing import Optional, List, Dict, Any, Union
from src.repositories.base_repository import BaseRepository
from src.models.products.product_model import Produto

class ProductRepository(BaseRepository[Dict[str, Any]]):
    """Repositório de produtos com operações CRUD e filtros avançados."""
    
    def __init__(self):
        # Garante que a conexão seja criada
        super().__init__()

    def _adaptar_para_dict(self, obj: Union[Produto, Dict]) -> Dict:
        """Helper para converter Objeto Produto em Dicionário."""
        if isinstance(obj, dict):
            return obj
        
        # Extrai dados do objeto Produto
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
        """Salva um novo produto."""
        # Converte objeto para dict se necessário
        obj = self._adaptar_para_dict(obj_entrada)

        # SQLite usa ? em vez de %s
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
    
    def buscar_por_id(self, id: int) -> Optional[Dict[str, Any]]:
        """Busca um produto por ID."""
        query = "SELECT * FROM produtos WHERE id = ?"
        
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def listar(self, limit: Optional[int] = None, offset: int = 0) -> List[Dict[str, Any]]:
        """Lista produtos com JOIN na categoria para a tela."""
        # Adicionamos o JOIN para que a tela possa mostrar o nome da categoria
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
        query = "DELETE FROM produtos WHERE id = ?"
        
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (id,))
            conn.commit()
            return cursor.rowcount > 0