"""Repositório para gerenciamento de produtos.

Implementa operações CRUD para a tabela produtos, com métodos
avançados de busca e filtros.
"""
from typing import Optional, List, Dict, Any
from .base_repository import BaseRepository


class ProdutoRepository(BaseRepository[Dict[str, Any]]):
    """Repositório de produtos com operações CRUD e filtros avançados."""
    
    def salvar(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """Salva um novo produto."""
        query = """
            INSERT INTO produtos 
            (nome, descricao, preco, sku, categoria_id, estoque, ativo)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        
        with self._conn_factory() as conn:
            cursor = conn.execute(
                query,
                (
                    obj['nome'],
                    obj.get('descricao'),
                    obj['preco'],
                    obj['sku'],
                    obj.get('categoria_id'),
                    obj.get('estoque', 0),
                    obj.get('ativo', 1)
                )
            )
            conn.commit()
            obj['id'] = cursor.lastrowid
        
        return obj
    
    def buscar_por_id(self, id: int) -> Optional[Dict[str, Any]]:
        """Busca um produto por ID."""
        query = "SELECT * FROM produtos WHERE id = ?"
        
        with self._conn_factory() as conn:
            cursor = conn.execute(query, (id,))
            row = cursor.fetchone()
            return self._row_to_dict(row) if row else None
    
    def listar(self, limit: Optional[int] = None, offset: int = 0) -> List[Dict[str, Any]]:
        """Lista todos os produtos."""
        query = "SELECT * FROM produtos ORDER BY criado_em DESC"
        
        if limit is not None:
            query += f" LIMIT {limit} OFFSET {offset}"
        
        with self._conn_factory() as conn:
            cursor = conn.execute(query)
            rows = cursor.fetchall()
            return [self._row_to_dict(row) for row in rows]
    
    def atualizar(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza um produto."""
        if 'id' not in obj:
            raise ValueError("Produto deve ter um ID para ser atualizado")
        
        query = """
            UPDATE produtos
            SET nome = ?, descricao = ?, preco = ?, sku = ?,
                categoria_id = ?, estoque = ?, ativo = ?
            WHERE id = ?
        """
        
        with self._conn_factory() as conn:
            conn.execute(
                query,
                (
                    obj['nome'],
                    obj.get('descricao'),
                    obj['preco'],
                    obj['sku'],
                    obj.get('categoria_id'),
                    obj.get('estoque', 0),
                    obj.get('ativo', 1),
                    obj['id']
                )
            )
            conn.commit()
        
        return obj
    
    def deletar(self, id: int) -> bool:
        """Deleta um produto por ID."""
        query = "DELETE FROM produtos WHERE id = ?"
        
        with self._conn_factory() as conn:
            cursor = conn.execute(query, (id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def buscar_por_sku(self, sku: str) -> Optional[Dict[str, Any]]:
        """Busca um produto por SKU.
        
        Args:
            sku: SKU do produto
            
        Returns:
            Produto ou None
        """
        query = "SELECT * FROM produtos WHERE sku = ?"
        
        with self._conn_factory() as conn:
            cursor = conn.execute(query, (sku,))
            row = cursor.fetchone()
            return self._row_to_dict(row) if row else None
    
    def listar_por_categoria(self, categoria_id: int, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Lista produtos de uma categoria.
        
        Args:
            categoria_id: ID da categoria
            limit: Número máximo de produtos
            
        Returns:
            Lista de produtos da categoria
        """
        query = "SELECT * FROM produtos WHERE categoria_id = ? AND ativo = 1 ORDER BY nome"
        
        if limit is not None:
            query += f" LIMIT {limit}"
        
        with self._conn_factory() as conn:
            cursor = conn.execute(query, (categoria_id,))
            rows = cursor.fetchall()
            return [self._row_to_dict(row) for row in rows]
    
    def buscar_com_filtros(
        self,
        busca: Optional[str] = None,
        categoria_id: Optional[int] = None,
        preco_min: Optional[float] = None,
        preco_max: Optional[float] = None,
        limit: int = 20,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """Busca produtos com filtros avançados.
        
        Args:
            busca: Termo de busca (nome ou descrição)
            categoria_id: Filtrar por categoria
            preco_min: Preço mínimo
            preco_max: Preço máximo
            limit: Número máximo de resultados
            offset: Offset para paginação
            
        Returns:
            Lista de produtos que atendem aos filtros
        """
        query = "SELECT * FROM produtos WHERE ativo = 1"
        params = []
        
        if busca:
            query += " AND (nome LIKE ? OR descricao LIKE ?)"
            busca_param = f"%{busca}%"
            params.extend([busca_param, busca_param])
        
        if categoria_id:
            query += " AND categoria_id = ?"
            params.append(categoria_id)
        
        if preco_min is not None:
            query += " AND preco >= ?"
            params.append(preco_min)
        
        if preco_max is not None:
            query += " AND preco <= ?"
            params.append(preco_max)
        
        query += " ORDER BY nome LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
        with self._conn_factory() as conn:
            cursor = conn.execute(query, params)
            rows = cursor.fetchall()
            return [self._row_to_dict(row) for row in rows]
    
    def atualizar_estoque(self, produto_id: int, quantidade: int) -> bool:
        """Atualiza o estoque de um produto.
        
        Args:
            produto_id: ID do produto
            quantidade: Nova quantidade em estoque
            
        Returns:
            True se atualizado com sucesso
        """
        query = "UPDATE produtos SET estoque = ? WHERE id = ?"
        
        with self._conn_factory() as conn:
            cursor = conn.execute(query, (quantidade, produto_id))
            conn.commit()
            return cursor.rowcount > 0
    
    def decrementar_estoque(self, produto_id: int, quantidade: int) -> bool:
        """Decrementa o estoque de um produto.
        
        Args:
            produto_id: ID do produto
            quantidade: Quantidade a decrementar
            
        Returns:
            True se atualizado com sucesso
            
        Raises:
            ValueError: Se estoque insuficiente
        """
        with self._conn_factory() as conn:
            # Verifica estoque atual
            produto = self.buscar_por_id(produto_id)
            if not produto:
                raise ValueError(f"Produto {produto_id} não encontrado")
            
            if produto['estoque'] < quantidade:
                raise ValueError(f"Estoque insuficiente. Disponível: {produto['estoque']}, Solicitado: {quantidade}")
            
            # Decrementa
            query = "UPDATE produtos SET estoque = estoque - ? WHERE id = ?"
            cursor = conn.execute(query, (quantidade, produto_id))
            conn.commit()
            return cursor.rowcount > 0
