"""Repositório para gerenciamento de produtos.
Implementa operações CRUD para a tabela produtos.
"""
from typing import Optional, List, Dict, Any, Union
from src.repositories.base_repository import BaseRepository
from src.models.products.product_model import Produto

class ProductRepository(BaseRepository[Dict[str, Any]]):
    """Repositório de produtos com operações CRUD e filtros avançados."""
    
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

    # --- MÉTODOS CRUD PADRÃO ---

    def salvar(self, obj_entrada: Union[Produto, Dict]) -> Dict[str, Any]:
        obj = self._adaptar_para_dict(obj_entrada)
        query = """
            INSERT INTO produtos (nome, descricao, preco, sku, categoria_id, estoque, ativo)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (
                obj['nome'], obj.get('descricao'), obj['preco'], obj['sku'],
                obj.get('categoria_id'), obj.get('estoque', 0), obj.get('ativo', 1)
            ))
            conn.commit()
            obj['id'] = cursor.lastrowid
        return obj
    
    def buscar_por_id(self, id: int) -> Optional[Dict[str, Any]]:
        query = "SELECT * FROM produtos WHERE id = ?"
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (id,))
            row = cursor.fetchone()
            return dict(row) if row else None
            
    def listar(self, limit: Optional[int] = None, offset: int = 0) -> List[Dict[str, Any]]:
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
        obj = self._adaptar_para_dict(obj_entrada)
        query = """
            UPDATE produtos
            SET nome = ?, descricao = ?, preco = ?, sku = ?,
                categoria_id = ?, estoque = ?, ativo = ?
            WHERE id = ?
        """
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (
                obj['nome'], obj.get('descricao'), obj['preco'], obj['sku'],
                obj.get('categoria_id'), obj.get('estoque', 0),
                obj.get('ativo', 1), obj['id']
            ))
            conn.commit()
        return obj
    
    def deletar(self, id: int) -> bool:
        query = "DELETE FROM produtos WHERE id = ?"
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (id,))
            conn.commit()
            return cursor.rowcount > 0

    # --- NOVO: MÉTODOS PARA TRANSAÇÃO (CHECKOUT) ---

    def buscar_por_id_para_bloqueio(self, id: int, conexao) -> Dict[str, Any]:
        """
        Busca produto usando uma conexão existente (transação).
        Em bancos reais usaria 'FOR UPDATE', no SQLite apenas garante leitura na mesma transação.
        """
        query = "SELECT * FROM produtos WHERE id = ?"
        cursor = conexao.cursor()
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        if not row:
            raise ValueError(f"Produto {id} não encontrado durante checkout.")
        return dict(row)

    def atualizar_estoque(self, id: int, novo_estoque: int, conexao) -> None:
        """Atualiza apenas o estoque usando uma conexão existente."""
        query = "UPDATE produtos SET estoque = ? WHERE id = ?"
        cursor = conexao.cursor()
        cursor.execute(query, (novo_estoque, id))