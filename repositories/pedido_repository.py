"""Repositório para gerenciamento de pedidos.

Implementa operações CRUD para pedidos e itens de pedido.
"""
from typing import Optional, List, Dict, Any
from .base_repository import BaseRepository


class PedidoRepository(BaseRepository[Dict[str, Any]]):
    """Repositório de pedidos com operações CRUD e gerenciamento de itens."""
    
    def salvar(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """Salva um novo pedido.
        
        Args:
            obj: Dicionário com dados do pedido
            
        Returns:
            Pedido salvo com ID atribuído
        """
        query = """
            INSERT INTO pedidos 
            (usuario_id, endereco_id, subtotal, frete, total, status, tipo_pagamento, observacoes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        with self._conn_factory() as conn:
            cursor = conn.execute(
                query,
                (
                    obj['usuario_id'],
                    obj['endereco_id'],
                    obj['subtotal'],
                    obj['frete'],
                    obj['total'],
                    obj.get('status', 'PENDENTE'),
                    obj['tipo_pagamento'],
                    obj.get('observacoes')
                )
            )
            conn.commit()
            obj['id'] = cursor.lastrowid
        
        return obj
    
    def buscar_por_id(self, id: int) -> Optional[Dict[str, Any]]:
        """Busca um pedido por ID."""
        query = "SELECT * FROM pedidos WHERE id = ?"
        
        with self._conn_factory() as conn:
            cursor = conn.execute(query, (id,))
            row = cursor.fetchone()
            return self._row_to_dict(row) if row else None
    
    def listar(self, limit: Optional[int] = None, offset: int = 0) -> List[Dict[str, Any]]:
        """Lista todos os pedidos."""
        query = "SELECT * FROM pedidos ORDER BY criado_em DESC"
        
        if limit is not None:
            query += f" LIMIT {limit} OFFSET {offset}"
        
        with self._conn_factory() as conn:
            cursor = conn.execute(query)
            rows = cursor.fetchall()
            return [self._row_to_dict(row) for row in rows]
    
    def atualizar(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza um pedido (geralmente apenas status)."""
        if 'id' not in obj:
            raise ValueError("Pedido deve ter um ID para ser atualizado")
        
        query = """
            UPDATE pedidos
            SET status = ?, observacoes = ?
            WHERE id = ?
        """
        
        with self._conn_factory() as conn:
            conn.execute(
                query,
                (obj.get('status', 'PENDENTE'), obj.get('observacoes'), obj['id'])
            )
            conn.commit()
        
        return obj
    
    def deletar(self, id: int) -> bool:
        """Deleta um pedido (cuidado: pode não ser permitido em produção)."""
        query = "DELETE FROM pedidos WHERE id = ?"
        
        with self._conn_factory() as conn:
            cursor = conn.execute(query, (id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def adicionar_item(
        self,
        pedido_id: int,
        produto_id: int,
        nome_produto: str,
        quantidade: int,
        preco_unitario: float
    ) -> Dict[str, Any]:
        """Adiciona um item ao pedido.
        
        Args:
            pedido_id: ID do pedido
            produto_id: ID do produto
            nome_produto: Nome do produto (snapshot no momento da compra)
            quantidade: Quantidade comprada
            preco_unitario: Preço unitário no momento da compra
            
        Returns:
            Item adicionado
        """
        subtotal = quantidade * preco_unitario
        
        query = """
            INSERT INTO itens_pedido 
            (pedido_id, produto_id, nome_produto, quantidade, preco_unitario, subtotal)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        
        with self._conn_factory() as conn:
            cursor = conn.execute(
                query,
                (pedido_id, produto_id, nome_produto, quantidade, preco_unitario, subtotal)
            )
            conn.commit()
            
            return {
                'id': cursor.lastrowid,
                'pedido_id': pedido_id,
                'produto_id': produto_id,
                'nome_produto': nome_produto,
                'quantidade': quantidade,
                'preco_unitario': preco_unitario,
                'subtotal': subtotal
            }
    
    def listar_itens(self, pedido_id: int) -> List[Dict[str, Any]]:
        """Lista todos os itens de um pedido.
        
        Args:
            pedido_id: ID do pedido
            
        Returns:
            Lista de itens do pedido
        """
        query = """
            SELECT * FROM itens_pedido
            WHERE pedido_id = ?
            ORDER BY id
        """
        
        with self._conn_factory() as conn:
            cursor = conn.execute(query, (pedido_id,))
            rows = cursor.fetchall()
            return [self._row_to_dict(row) for row in rows]
    
    def buscar_completo(self, pedido_id: int) -> Optional[Dict[str, Any]]:
        """Busca um pedido com todos os detalhes (itens, endereço, usuário).
        
        Args:
            pedido_id: ID do pedido
            
        Returns:
            Dicionário com pedido completo ou None
        """
        pedido = self.buscar_por_id(pedido_id)
        if not pedido:
            return None
        
        # Busca itens do pedido
        pedido['itens'] = self.listar_itens(pedido_id)
        
        # Busca dados do endereço
        query_endereco = """
            SELECT e.* FROM enderecos e
            WHERE e.id = ?
        """
        
        with self._conn_factory() as conn:
            cursor = conn.execute(query_endereco, (pedido['endereco_id'],))
            endereco = cursor.fetchone()
            pedido['endereco'] = self._row_to_dict(endereco) if endereco else None
        
        return pedido
    
    def listar_por_usuario(
        self,
        usuario_id: int,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """Lista pedidos de um usuário.
        
        Args:
            usuario_id: ID do usuário
            limit: Número máximo de pedidos
            offset: Offset para paginação
            
        Returns:
            Lista de pedidos do usuário
        """
        query = "SELECT * FROM pedidos WHERE usuario_id = ? ORDER BY criado_em DESC"
        
        if limit is not None:
            query += f" LIMIT {limit} OFFSET {offset}"
        
        with self._conn_factory() as conn:
            cursor = conn.execute(query, (usuario_id,))
            rows = cursor.fetchall()
            return [self._row_to_dict(row) for row in rows]
    
    def listar_por_status(
        self,
        status: str,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """Lista pedidos por status.
        
        Args:
            status: Status do pedido (PENDENTE, PROCESSANDO, ENVIADO, ENTREGUE, CANCELADO)
            limit: Número máximo de pedidos
            offset: Offset para paginação
            
        Returns:
            Lista de pedidos com o status especificado
        """
        query = "SELECT * FROM pedidos WHERE status = ? ORDER BY criado_em DESC"
        
        if limit is not None:
            query += f" LIMIT {limit} OFFSET {offset}"
        
        with self._conn_factory() as conn:
            cursor = conn.execute(query, (status,))
            rows = cursor.fetchall()
            return [self._row_to_dict(row) for row in rows]
    
    def atualizar_status(self, pedido_id: int, novo_status: str) -> bool:
        """Atualiza o status de um pedido.
        
        Args:
            pedido_id: ID do pedido
            novo_status: Novo status
            
        Returns:
            True se atualizado com sucesso
        """
        query = "UPDATE pedidos SET status = ? WHERE id = ?"
        
        with self._conn_factory() as conn:
            cursor = conn.execute(query, (novo_status, pedido_id))
            conn.commit()
            return cursor.rowcount > 0
    
    def contar_por_status(self, status: str) -> int:
        """Conta pedidos por status.
        
        Args:
            status: Status do pedido
            
        Returns:
            Número de pedidos com o status
        """
        query = "SELECT COUNT(*) as total FROM pedidos WHERE status = ?"
        
        with self._conn_factory() as conn:
            cursor = conn.execute(query, (status,))
            row = cursor.fetchone()
            return row['total'] if row else 0
    
    def calcular_total_vendas(self, usuario_id: Optional[int] = None) -> float:
        """Calcula o total de vendas (pedidos ENTREGUE).
        
        Args:
            usuario_id: Opcional, filtrar por usuário
            
        Returns:
            Total de vendas
        """
        if usuario_id:
            query = """
                SELECT SUM(total) as total_vendas 
                FROM pedidos 
                WHERE status = 'ENTREGUE' AND usuario_id = ?
            """
            params = (usuario_id,)
        else:
            query = "SELECT SUM(total) as total_vendas FROM pedidos WHERE status = 'ENTREGUE'"
            params = ()
        
        with self._conn_factory() as conn:
            cursor = conn.execute(query, params)
            row = cursor.fetchone()
            return row['total_vendas'] if row and row['total_vendas'] else 0.0
