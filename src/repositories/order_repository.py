"""Repositório para gerenciamento de pedidos.

Implementa operações CRUD para pedidos e itens de pedido.
"""
from typing import Optional, List, Dict, Any
from .base_repository import BaseRepository
from src.models.sales.order_model import Pedido 

class PedidoRepository(BaseRepository[Dict[str, Any]]):
    """Repositório de pedidos com operações CRUD e gerenciamento de itens."""
    
    def salvar(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """Salva um novo pedido (Método padrão)."""
        query = """
            INSERT INTO pedidos 
            (usuario_id, endereco_id, subtotal, frete, total, status, tipo_pagamento, observacoes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(
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

    def salvar_pedido_e_itens(self, pedido: Pedido, conexao) -> None:
        """Salva o Pedido e seus Itens usando uma conexão de transação JÁ ABERTA."""
        cursor = conexao.cursor()
        
        query_pedido = """
            INSERT INTO pedidos 
            (usuario_id, endereco_id, subtotal, frete, total, status, tipo_pagamento, observacoes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        frete = getattr(pedido, 'frete', 0.0)
        total = pedido.valor_total
        subtotal = total - frete
        tipo_pag = pedido.tipo_pagamento 
        
        cursor.execute(query_pedido, (
            pedido.cliente_id,
            pedido.endereco_entrega_id,
            subtotal,
            frete,
            total,
            pedido.status,
            tipo_pag, 
            ""
        ))
        
        pedido_id = cursor.lastrowid
        
        if hasattr(pedido, 'id'):
            try: pedido.id = pedido_id
            except: pass 
        if hasattr(pedido, '_id'):
            pedido._id = pedido_id

        query_item = """
            INSERT INTO itens_pedido 
            (pedido_id, produto_id, nome_produto, quantidade, preco_unitario, subtotal)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        
        for item in pedido.itens:
            prod_id = item.produto.id
            cursor.execute("SELECT nome FROM produtos WHERE id = ?", (prod_id,))
            row = cursor.fetchone()
            nome_produto = row[0] if row else "Produto Desconhecido"
            
            subtotal_item = item.quantidade * item.preco_unitario
            
            cursor.execute(query_item, (
                pedido_id, prod_id, nome_produto,
                item.quantidade, item.preco_unitario, subtotal_item
            ))

    # --- MÉTODOS DE LEITURA (CORRIGIDOS PARA USAR VIEW) ---

    def buscar_por_id(self, id: int) -> Optional[Dict[str, Any]]:
        query = "SELECT * FROM pedidos WHERE id = ?"
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def listar(self, limit: Optional[int] = None, offset: int = 0) -> List[Dict[str, Any]]:
        """Lista todos os pedidos usando a VIEW detalhada."""
        query = "SELECT * FROM vw_pedidos_detalhados ORDER BY criado_em DESC"
        
        params = []
        if limit is not None:
            query += " LIMIT ? OFFSET ?"
            params.extend([limit, offset])
        
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, tuple(params))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def listar_por_status(self, status: str, limit: Optional[int] = None, offset: int = 0) -> List[Dict[str, Any]]:
        """Lista pedidos por status usando a VIEW detalhada."""
        query = "SELECT * FROM vw_pedidos_detalhados WHERE status = ? ORDER BY criado_em DESC"
        
        params = [status]
        if limit is not None:
            query += " LIMIT ? OFFSET ?"
            params.extend([limit, offset])
        
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, tuple(params))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def atualizar(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        if 'id' not in obj: raise ValueError("Pedido deve ter um ID")
        query = "UPDATE pedidos SET status = ?, observacoes = ? WHERE id = ?"
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (obj.get('status', 'PENDENTE'), obj.get('observacoes'), obj['id']))
            conn.commit()
        return obj
    
    def deletar(self, id: int) -> bool:
        query = "DELETE FROM pedidos WHERE id = ?"
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (id,))
            conn.commit()
            return cursor.rowcount > 0

    def listar_itens(self, pedido_id: int) -> List[Dict[str, Any]]:
        query = "SELECT * FROM itens_pedido WHERE pedido_id = ? ORDER BY id"
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (pedido_id,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def buscar_completo(self, pedido_id: int) -> Optional[Dict[str, Any]]:
        # Busca da View para já ter os dados do cliente
        query = "SELECT * FROM vw_pedidos_detalhados WHERE id = ?"
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (pedido_id,))
            row = cursor.fetchone()
            if not row: return None
            pedido = dict(row)
            
            # Busca itens
            pedido['itens'] = self.listar_itens(pedido_id)
            
            # Busca endereço
            cursor.execute("SELECT * FROM enderecos WHERE id = ?", (pedido['endereco_id'],))
            end_row = cursor.fetchone()
            pedido['endereco'] = dict(end_row) if end_row else None
            
            return pedido

    def listar_por_usuario(self, usuario_id: int, limit=None, offset=0) -> List[Dict[str, Any]]:
        query = "SELECT * FROM pedidos WHERE usuario_id = ? ORDER BY criado_em DESC"
        params = [usuario_id]
        if limit:
            query += " LIMIT ? OFFSET ?"
            params.extend([limit, offset])
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, tuple(params))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def atualizar_status(self, pedido_id: int, novo_status: str) -> bool:
        query = "UPDATE pedidos SET status = ? WHERE id = ?"
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (novo_status, pedido_id))
            conn.commit()
            return cursor.rowcount > 0
    
    def contar_por_status(self, status: str) -> int:
        query = "SELECT COUNT(*) as total FROM pedidos WHERE status = ?"
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (status,))
            row = cursor.fetchone()
            return row['total'] if row else 0
    
    def calcular_total_vendas(self, usuario_id=None) -> float:
        if usuario_id:
            query = "SELECT SUM(total) as total_vendas FROM pedidos WHERE status = 'ENTREGUE' AND usuario_id = ?"
            params = (usuario_id,)
        else:
            query = "SELECT SUM(total) as total_vendas FROM pedidos WHERE status = 'ENTREGUE'"
            params = ()
        with self._conn_factory() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            row = cursor.fetchone()
            return row['total_vendas'] if row and row['total_vendas'] else 0.0