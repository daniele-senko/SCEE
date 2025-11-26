"""Repositório para gerenciamento de endereços.

Implementa operações CRUD para a tabela enderecos.
"""
from typing import Optional, List, Dict, Any
from .base_repository import BaseRepository


class EnderecoRepository(BaseRepository[Dict[str, Any]]):
    """Repositório de endereços com operações CRUD completas."""
    
    def salvar(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """Salva um novo endereço.
        
        Args:
            obj: Dicionário com dados do endereço
            
        Returns:
            Endereço salvo com ID atribuído
        """
        query = """
            INSERT INTO enderecos 
            (usuario_id, logradouro, numero, complemento, bairro, cidade, estado, cep, principal)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(
                query,
                (
                    obj['usuario_id'],
                    obj['logradouro'],
                    obj['numero'],
                    obj.get('complemento'),
                    obj['bairro'],
                    obj['cidade'],
                    obj['estado'],
                    obj['cep'],
                    obj.get('principal', 0)
                )
            )
            conn.commit()
            obj['id'] = cursor.lastrowid
        
        return obj
    
    def buscar_por_id(self, id: int) -> Optional[Dict[str, Any]]:
        """Busca um endereço por ID."""
        query = "SELECT * FROM enderecos WHERE id = %s"
        
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (id,))
            row = cursor.fetchone()
            return row
    
    def listar(self, limit: Optional[int] = None, offset: int = 0) -> List[Dict[str, Any]]:
        """Lista todos os endereços."""
        query = "SELECT * FROM enderecos ORDER BY criado_em DESC"
        
        if limit is not None:
            query += f" LIMIT {limit} OFFSET {offset}"
        
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
    
    def atualizar(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza um endereço."""
        if 'id' not in obj:
            raise ValueError("Endereço deve ter um ID para ser atualizado")
        
        query = """
            UPDATE enderecos
            SET logradouro = %s, numero = %s, complemento = %s, bairro = %s,
                cidade = %s, estado = %s, cep = %s, principal = %s
            WHERE id = %s
        """
        
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(
                query,
                (
                    obj['logradouro'],
                    obj['numero'],
                    obj.get('complemento'),
                    obj['bairro'],
                    obj['cidade'],
                    obj['estado'],
                    obj['cep'],
                    obj.get('principal', 0),
                    obj['id']
                )
            )
            conn.commit()
        
        return obj
    
    def deletar(self, id: int) -> bool:
        """Deleta um endereço por ID."""
        query = "DELETE FROM enderecos WHERE id = %s"
        
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def listar_por_usuario(self, usuario_id: int) -> List[Dict[str, Any]]:
        """Lista todos os endereços de um usuário.
        
        Args:
            usuario_id: ID do usuário
            
        Returns:
            Lista de endereços do usuário
        """
        query = "SELECT * FROM enderecos WHERE usuario_id = %s ORDER BY principal DESC, criado_em DESC"
        
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (usuario_id,))
            rows = cursor.fetchall()
            return rows
    
    def buscar_principal(self, usuario_id: int) -> Optional[Dict[str, Any]]:
        """Busca o endereço principal de um usuário.
        
        Args:
            usuario_id: ID do usuário
            
        Returns:
            Endereço principal ou None
        """
        query = "SELECT * FROM enderecos WHERE usuario_id = %s AND principal = 1 LIMIT 1"
        
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (usuario_id,))
            row = cursor.fetchone()
            return row
    
    def definir_principal(self, id: int, usuario_id: int) -> bool:
        """Define um endereço como principal (e desmarca os outros).
        
        Args:
            id: ID do endereço a ser marcado como principal
            usuario_id: ID do usuário (para validação)
            
        Returns:
            True se atualizado com sucesso
        """
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            # Desmarca todos os endereços como não-principais
            cursor.execute(
                "UPDATE enderecos SET principal = 0 WHERE usuario_id = %s",
                (usuario_id,)
            )
            
            # Marca o endereço especificado como principal
            cursor.execute(
                "UPDATE enderecos SET principal = 1 WHERE id = %s AND usuario_id = %s",
                (id, usuario_id)
            )
            
            conn.commit()
            return cursor.rowcount > 0
