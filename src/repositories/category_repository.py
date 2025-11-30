"""Repositório de Categorias."""
from typing import List, Dict, Any, Optional, Union
from src.repositories.base_repository import BaseRepository

class CategoryRepository(BaseRepository[Dict[str, Any]]):
    """
    Gerencia o acesso a dados da tabela 'categorias'.
    """
    
    def __init__(self):
        super().__init__()

    def salvar(self, categoria: Dict[str, Any]) -> Dict[str, Any]:
        """Cadastra uma nova categoria."""
        query = """
            INSERT INTO categorias (nome, descricao, ativo)
            VALUES (?, ?, ?)
        """
        params = (
            categoria['nome'],
            categoria.get('descricao', ''),
            categoria.get('ativo', 1)
        )
        
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            categoria['id'] = cursor.lastrowid
            
        return categoria

    def atualizar(self, categoria: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza dados de uma categoria."""
        query = """
            UPDATE categorias 
            SET nome = ?, descricao = ?, ativo = ?
            WHERE id = ?
        """
        params = (
            categoria['nome'],
            categoria.get('descricao', ''),
            categoria.get('ativo', 1),
            categoria['id']
        )
        
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            
        return categoria

    def listar(self) -> List[Dict[str, Any]]:
        """Lista todas as categorias."""
        query = "SELECT * FROM categorias ORDER BY nome"
        
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def buscar_por_id(self, id: int) -> Optional[Dict[str, Any]]:
        """Busca categoria por ID."""
        query = "SELECT * FROM categorias WHERE id = ?"
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (id,))
            row = cursor.fetchone()
            return dict(row) if row else None
            
    def buscar_por_nome(self, nome: str) -> Optional[Dict[str, Any]]:
        """Busca categoria por Nome (para evitar duplicatas)."""
        query = "SELECT * FROM categorias WHERE nome = ?"
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (nome,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def deletar(self, id: int) -> bool:
        """Deleta (ou desativa) uma categoria."""
        query = "DELETE FROM categorias WHERE id = ?"
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (id,))
            conn.commit()
            return cursor.rowcount > 0