"""Repositório para gerenciamento de usuários.

Implementa operações CRUD para a tabela usuarios, incluindo
métodos específicos como busca por email.
"""
from typing import Optional, List, Dict, Any
from .base_repository import BaseRepository


class UsuarioRepository(BaseRepository[Dict[str, Any]]):
    """Repositório de usuários com operações CRUD completas."""
    
    def salvar(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """Salva um novo usuário no banco de dados.
        
        Args:
            obj: Dicionário com dados do usuário (nome, email, senha_hash, tipo)
            
        Returns:
            Usuário salvo com ID atribuído
        """
        query = """
            INSERT INTO usuarios (nome, email, senha_hash, tipo)
            VALUES (%s, %s, %s, %s)
        """
        
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(
                query,
                (obj['nome'], obj['email'], obj['senha_hash'], obj.get('tipo', 'cliente'))
            )
            conn.commit()
            obj['id'] = cursor.lastrowid
        
        return obj
    
    def buscar_por_id(self, id: int) -> Optional[Dict[str, Any]]:
        """Busca um usuário por ID.
        
        Args:
            id: ID do usuário
            
        Returns:
            Dicionário com dados do usuário ou None
        """
        query = "SELECT * FROM usuarios WHERE id = %s"
        
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (id,))
            row = cursor.fetchone()
            return row
    
    def listar(self, limit: Optional[int] = None, offset: int = 0) -> List[Dict[str, Any]]:
        """Lista todos os usuários com paginação.
        
        Args:
            limit: Número máximo de usuários a retornar
            offset: Número de registros a pular
            
        Returns:
            Lista de usuários
        """
        query = "SELECT * FROM usuarios ORDER BY criado_em DESC"
        
        if limit is not None:
            query += f" LIMIT {limit} OFFSET {offset}"
        
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
    
    def atualizar(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza um usuário existente.
        
        Args:
            obj: Dicionário com dados do usuário (deve conter 'id')
            
        Returns:
            Usuário atualizado
        """
        if 'id' not in obj:
            raise ValueError("Usuário deve ter um ID para ser atualizado")
        
        query = """
            UPDATE usuarios
            SET nome = %s, email = %s, tipo = %s
            WHERE id = %s
        """
        
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(
                query,
                (obj['nome'], obj['email'], obj.get('tipo', 'cliente'), obj['id'])
            )
            conn.commit()
        
        return obj
    
    def deletar(self, id: int) -> bool:
        """Deleta um usuário por ID.
        
        Args:
            id: ID do usuário
            
        Returns:
            True se deletado, False se não encontrado
        """
        query = "DELETE FROM usuarios WHERE id = %s"
        
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def buscar_por_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Busca um usuário por email (método específico do repositório).
        
        Args:
            email: Email do usuário
            
        Returns:
            Dicionário com dados do usuário ou None
        """
        query = "SELECT * FROM usuarios WHERE email = %s"
        
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (email,))
            row = cursor.fetchone()
            return row
    
    def contar_por_tipo(self, tipo: str) -> int:
        """Conta o número de usuários de um determinado tipo.
        
        Args:
            tipo: Tipo do usuário ('cliente' ou 'administrador')
            
        Returns:
            Número de usuários do tipo especificado
        """
        query = "SELECT COUNT(*) as total FROM usuarios WHERE tipo = %s"
        
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (tipo,))
            row = cursor.fetchone()
            return row['total'] if row else 0
