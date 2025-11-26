"""Repositório para gerenciamento de carrinhos de compra.

Implementa operações CRUD para carrinho e itens do carrinho.
"""
from typing import Optional, List, Dict, Any
from .base_repository import BaseRepository


class CarrinhoRepository(BaseRepository[Dict[str, Any]]):
    """Repositório de carrinhos com operações CRUD e gerenciamento de itens."""
    
    def salvar(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """Salva um novo carrinho."""
        query = "INSERT INTO carrinhos (usuario_id) VALUES (?)"
        
        with self._conn_factory() as conn:
            cursor = conn.execute(query, (obj['usuario_id'],))
            conn.commit()
            obj['id'] = cursor.lastrowid
        
        return obj
    
    def buscar_por_id(self, id: int) -> Optional[Dict[str, Any]]:
        """Busca um carrinho por ID."""
        query = "SELECT * FROM carrinhos WHERE id = ?"
        
        with self._conn_factory() as conn:
            cursor = conn.execute(query, (id,))
            row = cursor.fetchone()
            return self._row_to_dict(row) if row else None
    
    def listar(self, limit: Optional[int] = None, offset: int = 0) -> List[Dict[str, Any]]:
        """Lista todos os carrinhos."""
        query = "SELECT * FROM carrinhos ORDER BY atualizado_em DESC"
        
        if limit is not None:
            query += f" LIMIT {limit} OFFSET {offset}"
        
        with self._conn_factory() as conn:
            cursor = conn.execute(query)
            rows = cursor.fetchall()
            return [self._row_to_dict(row) for row in rows]
    
    def atualizar(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza um carrinho (normalmente apenas timestamp)."""
        if 'id' not in obj:
            raise ValueError("Carrinho deve ter um ID para ser atualizado")
        
        # A atualização do timestamp é automática via trigger
        return obj
    
    def deletar(self, id: int) -> bool:
        """Deleta um carrinho (e seus itens em cascata)."""
        query = "DELETE FROM carrinhos WHERE id = ?"
        
        with self._conn_factory() as conn:
            cursor = conn.execute(query, (id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def buscar_por_usuario(self, usuario_id: int) -> Optional[Dict[str, Any]]:
        """Busca o carrinho ativo de um usuário.
        
        Args:
            usuario_id: ID do usuário
            
        Returns:
            Carrinho do usuário ou None
        """
        query = "SELECT * FROM carrinhos WHERE usuario_id = ?"
        
        with self._conn_factory() as conn:
            cursor = conn.execute(query, (usuario_id,))
            row = cursor.fetchone()
            return self._row_to_dict(row) if row else None
    
    def obter_ou_criar(self, usuario_id: int) -> Dict[str, Any]:
        """Obtém o carrinho do usuário ou cria um novo se não existir.
        
        Args:
            usuario_id: ID do usuário
            
        Returns:
            Carrinho do usuário
        """
        carrinho = self.buscar_por_usuario(usuario_id)
        if not carrinho:
            carrinho = self.salvar({'usuario_id': usuario_id})
        return carrinho
    
    def adicionar_item(
        self,
        carrinho_id: int,
        produto_id: int,
        quantidade: int,
        preco_unitario: float
    ) -> Dict[str, Any]:
        """Adiciona um item ao carrinho.
        
        Args:
            carrinho_id: ID do carrinho
            produto_id: ID do produto
            quantidade: Quantidade a adicionar
            preco_unitario: Preço unitário do produto
            
        Returns:
            Item adicionado
        """
        # Verifica se o item já existe no carrinho
        query_check = """
            SELECT * FROM itens_carrinho 
            WHERE carrinho_id = ? AND produto_id = ?
        """
        
        with self._conn_factory() as conn:
            cursor = conn.execute(query_check, (carrinho_id, produto_id))
            item_existente = cursor.fetchone()
            
            if item_existente:
                # Atualiza quantidade
                nova_quantidade = item_existente['quantidade'] + quantidade
                query_update = """
                    UPDATE itens_carrinho
                    SET quantidade = ?, preco_unitario = ?
                    WHERE id = ?
                """
                conn.execute(query_update, (nova_quantidade, preco_unitario, item_existente['id']))
                conn.commit()
                
                return {
                    'id': item_existente['id'],
                    'carrinho_id': carrinho_id,
                    'produto_id': produto_id,
                    'quantidade': nova_quantidade,
                    'preco_unitario': preco_unitario
                }
            else:
                # Insere novo item
                query_insert = """
                    INSERT INTO itens_carrinho (carrinho_id, produto_id, quantidade, preco_unitario)
                    VALUES (?, ?, ?, ?)
                """
                cursor = conn.execute(query_insert, (carrinho_id, produto_id, quantidade, preco_unitario))
                conn.commit()
                
                return {
                    'id': cursor.lastrowid,
                    'carrinho_id': carrinho_id,
                    'produto_id': produto_id,
                    'quantidade': quantidade,
                    'preco_unitario': preco_unitario
                }
    
    def remover_item(self, item_id: int) -> bool:
        """Remove um item do carrinho.
        
        Args:
            item_id: ID do item a remover
            
        Returns:
            True se removido com sucesso
        """
        query = "DELETE FROM itens_carrinho WHERE id = ?"
        
        with self._conn_factory() as conn:
            cursor = conn.execute(query, (item_id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def atualizar_quantidade_item(self, item_id: int, quantidade: int) -> bool:
        """Atualiza a quantidade de um item no carrinho.
        
        Args:
            item_id: ID do item
            quantidade: Nova quantidade
            
        Returns:
            True se atualizado com sucesso
        """
        if quantidade <= 0:
            return self.remover_item(item_id)
        
        query = "UPDATE itens_carrinho SET quantidade = ? WHERE id = ?"
        
        with self._conn_factory() as conn:
            cursor = conn.execute(query, (quantidade, item_id))
            conn.commit()
            return cursor.rowcount > 0
    
    def listar_itens(self, carrinho_id: int) -> List[Dict[str, Any]]:
        """Lista todos os itens de um carrinho com informações dos produtos.
        
        Args:
            carrinho_id: ID do carrinho
            
        Returns:
            Lista de itens com detalhes dos produtos
        """
        query = """
            SELECT 
                ic.*,
                p.nome as produto_nome,
                p.descricao as produto_descricao,
                p.sku,
                p.estoque
            FROM itens_carrinho ic
            INNER JOIN produtos p ON ic.produto_id = p.id
            WHERE ic.carrinho_id = ?
            ORDER BY ic.criado_em DESC
        """
        
        with self._conn_factory() as conn:
            cursor = conn.execute(query, (carrinho_id,))
            rows = cursor.fetchall()
            return [self._row_to_dict(row) for row in rows]
    
    def calcular_total(self, carrinho_id: int) -> float:
        """Calcula o valor total do carrinho.
        
        Args:
            carrinho_id: ID do carrinho
            
        Returns:
            Valor total do carrinho
        """
        query = """
            SELECT SUM(quantidade * preco_unitario) as total
            FROM itens_carrinho
            WHERE carrinho_id = ?
        """
        
        with self._conn_factory() as conn:
            cursor = conn.execute(query, (carrinho_id,))
            row = cursor.fetchone()
            return row['total'] if row and row['total'] else 0.0
    
    def limpar(self, carrinho_id: int) -> bool:
        """Remove todos os itens de um carrinho.
        
        Args:
            carrinho_id: ID do carrinho
            
        Returns:
            True se items foram removidos
        """
        query = "DELETE FROM itens_carrinho WHERE carrinho_id = ?"
        
        with self._conn_factory() as conn:
            cursor = conn.execute(query, (carrinho_id,))
            conn.commit()
            return cursor.rowcount > 0
