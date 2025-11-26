"""Repositório para gerenciamento de clientes.

Implementa operações CRUD para a tabela clientes_info, com
métodos específicos como busca por CPF.
"""
from typing import Optional, List, Dict, Any
from .base_repository import BaseRepository


class ClienteRepository(BaseRepository[Dict[str, Any]]):
    """Repositório de clientes com operações CRUD completas."""
    
    def salvar(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """Salva informações de um novo cliente.
        
        Args:
            obj: Dicionário com dados do cliente (usuario_id, cpf, telefone, data_nascimento)
            
        Returns:
            Cliente salvo com ID atribuído
        """
        query = """
            INSERT INTO clientes_info (usuario_id, cpf, telefone, data_nascimento)
            VALUES (?, ?, ?, ?)
        """
        
        with self._conn_factory() as conn:
            cursor = conn.execute(
                query,
                (obj['usuario_id'], obj['cpf'], obj.get('telefone'), obj.get('data_nascimento'))
            )
            conn.commit()
            obj['id'] = cursor.lastrowid
        
        return obj
    
    def buscar_por_id(self, id: int) -> Optional[Dict[str, Any]]:
        """Busca um cliente por ID.
        
        Args:
            id: ID do cliente
            
        Returns:
            Dicionário com dados do cliente ou None
        """
        query = "SELECT * FROM clientes_info WHERE id = ?"
        
        with self._conn_factory() as conn:
            cursor = conn.execute(query, (id,))
            row = cursor.fetchone()
            return self._row_to_dict(row) if row else None
    
    def listar(self, limit: Optional[int] = None, offset: int = 0) -> List[Dict[str, Any]]:
        """Lista todos os clientes com paginação.
        
        Args:
            limit: Número máximo de clientes a retornar
            offset: Número de registros a pular
            
        Returns:
            Lista de clientes
        """
        query = "SELECT * FROM clientes_info ORDER BY criado_em DESC"
        
        if limit is not None:
            query += f" LIMIT {limit} OFFSET {offset}"
        
        with self._conn_factory() as conn:
            cursor = conn.execute(query)
            rows = cursor.fetchall()
            return [self._row_to_dict(row) for row in rows]
    
    def atualizar(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza informações de um cliente.
        
        Args:
            obj: Dicionário com dados do cliente (deve conter 'id')
            
        Returns:
            Cliente atualizado
        """
        if 'id' not in obj:
            raise ValueError("Cliente deve ter um ID para ser atualizado")
        
        query = """
            UPDATE clientes_info
            SET cpf = ?, telefone = ?, data_nascimento = ?
            WHERE id = ?
        """
        
        with self._conn_factory() as conn:
            conn.execute(
                query,
                (obj['cpf'], obj.get('telefone'), obj.get('data_nascimento'), obj['id'])
            )
            conn.commit()
        
        return obj
    
    def deletar(self, id: int) -> bool:
        """Deleta um cliente por ID.
        
        Args:
            id: ID do cliente
            
        Returns:
            True se deletado, False se não encontrado
        """
        query = "DELETE FROM clientes_info WHERE id = ?"
        
        with self._conn_factory() as conn:
            cursor = conn.execute(query, (id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def buscar_por_cpf(self, cpf: str) -> Optional[Dict[str, Any]]:
        """Busca um cliente por CPF.
        
        Args:
            cpf: CPF do cliente
            
        Returns:
            Dicionário com dados do cliente ou None
        """
        query = "SELECT * FROM clientes_info WHERE cpf = ?"
        
        with self._conn_factory() as conn:
            cursor = conn.execute(query, (cpf,))
            row = cursor.fetchone()
            return self._row_to_dict(row) if row else None
    
    def buscar_por_usuario_id(self, usuario_id: int) -> Optional[Dict[str, Any]]:
        """Busca um cliente por ID do usuário.
        
        Args:
            usuario_id: ID do usuário associado
            
        Returns:
            Dicionário com dados do cliente ou None
        """
        query = "SELECT * FROM clientes_info WHERE usuario_id = ?"
        
        with self._conn_factory() as conn:
            cursor = conn.execute(query, (usuario_id,))
            row = cursor.fetchone()
            return self._row_to_dict(row) if row else None
    
    def buscar_completo(self, usuario_id: int) -> Optional[Dict[str, Any]]:
        """Busca dados completos do cliente (usuário + cliente_info).
        
        Args:
            usuario_id: ID do usuário
            
        Returns:
            Dicionário com dados completos ou None
        """
        query = """
            SELECT 
                u.id, u.nome, u.email, u.tipo,
                c.cpf, c.telefone, c.data_nascimento
            FROM usuarios u
            INNER JOIN clientes_info c ON u.id = c.usuario_id
            WHERE u.id = ?
        """
        
        with self._conn_factory() as conn:
            cursor = conn.execute(query, (usuario_id,))
            row = cursor.fetchone()
            return self._row_to_dict(row) if row else None
