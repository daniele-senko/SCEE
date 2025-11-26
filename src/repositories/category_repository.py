"""Repositório para gerenciamento de categorias.

Implementa operações CRUD para a tabela categorias.
"""
from typing import Optional, List, Dict, Any
from .base_repository import BaseRepository


class CategoriaRepository(BaseRepository[Dict[str, Any]]):
    """Repositório de categorias com operações CRUD completas."""
    
    def salvar(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """Salva uma nova categoria."""
        query = """
            INSERT INTO categorias (nome, descricao, ativo)
            VALUES (%s, %s, %s)
        """
        
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(
                query,
                (obj['nome'], obj.get('descricao'), obj.get('ativo', 1))
            )
            conn.commit()
            obj['id'] = cursor.lastrowid
        
        return obj
    
    def buscar_por_id(self, id: int) -> Optional[Dict[str, Any]]:
        """Busca uma categoria por ID."""
        query = "SELECT * FROM categorias WHERE id = %s"
        
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (id,))
            row = cursor.fetchone()
            return row
    
    def listar(self, limit: Optional[int] = None, offset: int = 0) -> List[Dict[str, Any]]:
        """Lista todas as categorias."""
        query = "SELECT * FROM categorias ORDER BY nome"
        
        if limit is not None:
            query += f" LIMIT {limit} OFFSET {offset}"
        
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
    
    def atualizar(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza uma categoria."""
        if 'id' not in obj:
            raise ValueError("Categoria deve ter um ID para ser atualizada")
        
        query = """
            UPDATE categorias
            SET nome = %s, descricao = %s, ativo = %s
            WHERE id = %s
        """
        
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(
                query,
                (obj['nome'], obj.get('descricao'), obj.get('ativo', 1), obj['id'])
            )
            conn.commit()
        
        return obj
    
    def deletar(self, id: int) -> bool:
        """Deleta uma categoria por ID."""
        query = "DELETE FROM categorias WHERE id = %s"
        
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def listar_ativas(self) -> List[Dict[str, Any]]:
        """Lista apenas categorias ativas.
        
        Returns:
            Lista de categorias ativas
        """
        query = "SELECT * FROM categorias WHERE ativo = 1 ORDER BY nome"
        
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
    
    def buscar_por_nome(self, nome: str) -> Optional[Dict[str, Any]]:
        """Busca uma categoria por nome.
        
        Args:
            nome: Nome da categoria
            
        Returns:
            Categoria ou None
        """
        query = "SELECT * FROM categorias WHERE nome = %s"
        
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (nome,))
            row = cursor.fetchone()
            return row
