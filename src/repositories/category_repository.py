"""Repositório para gerenciamento de categorias.
Implementa operações CRUD para a tabela categorias.
"""
from typing import Optional, List, Dict, Any, Union
from src.repositories.base_repository import BaseRepository
from src.models.products.category_model import Categoria

class CategoriaRepository(BaseRepository[Dict[str, Any]]):
    """Repositório de categorias com operações CRUD completas."""
    
    def __init__(self):
        super().__init__()

    def _adaptar_para_dict(self, obj: Union[Categoria, Dict]) -> Dict:
        """
        Método auxiliar que converte Objeto -> Dicionário.
        Resolve o conflito entre POO e o código legado.
        """
        if isinstance(obj, dict):
            return obj
            
        # Se for um objeto Categoria, transforma em dict
        return {
            "id": getattr(obj, "id", None),
            "nome": getattr(obj, "nome", ""),
            # Define valores padrão se o objeto não tiver esses atributos
            "descricao": getattr(obj, "descricao", ""), 
            "ativo": getattr(obj, "ativo", 1)
        }

    def salvar(self, obj_entrada: Union[Categoria, Dict]) -> Dict[str, Any]:
        """Salva uma nova categoria (Aceita Objeto ou Dict)."""
        
        # Converte para o formato que o código do seu amigo entende (Dict)
        obj = self._adaptar_para_dict(obj_entrada)

        query = """
            INSERT INTO categorias (nome, descricao, ativo)
            VALUES (?, ?, ?)
        """
        
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(
                query,
                (obj['nome'], obj.get('descricao', ''), obj.get('ativo', 1))
            )
            conn.commit()
            obj['id'] = cursor.lastrowid
            
            # Se a entrada foi um Objeto, atualizamos o ID dele também
            if hasattr(obj_entrada, '_id'): 
                obj_entrada._id = cursor.lastrowid
        
        return obj
    
    def buscar_por_id(self, id: int) -> Optional[Dict[str, Any]]:
        query = "SELECT * FROM categorias WHERE id = ?"
        
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def listar(self, limit: Optional[int] = None, offset: int = 0) -> List[Dict[str, Any]]:
        query = "SELECT * FROM categorias ORDER BY nome"
        
        params = []
        if limit is not None:
            query += " LIMIT ? OFFSET ?"
            params.extend([limit, offset])
        
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, tuple(params))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def atualizar(self, obj_entrada: Union[Categoria, Dict]) -> Dict[str, Any]:
        obj = self._adaptar_para_dict(obj_entrada)
        
        if 'id' not in obj or not obj['id']:
            raise ValueError("Categoria deve ter um ID para ser atualizada")
        
        query = """
            UPDATE categorias
            SET nome = ?, descricao = ?, ativo = ?
            WHERE id = ?
        """
        
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(
                query,
                (obj['nome'], obj.get('descricao', ''), obj.get('ativo', 1), obj['id'])
            )
            conn.commit()
        
        return obj
    
    def deletar(self, id: int) -> bool:
        query = "DELETE FROM categorias WHERE id = ?"
        
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def listar_ativas(self) -> List[Dict[str, Any]]:
        query = "SELECT * FROM categorias WHERE ativo = 1 ORDER BY nome"
        
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def buscar_por_nome(self, nome: str) -> Optional[Dict[str, Any]]:
        query = "SELECT * FROM categorias WHERE nome = ?"
        
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (nome,))
            row = cursor.fetchone()
            return dict(row) if row else None