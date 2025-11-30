"""
AdminController - Controlador de Administração
==============================================

Gerencia operações administrativas.
"""
from typing import Dict, Any, Optional
from src.controllers.base_controller import BaseController
from src.services.catalog_service import CatalogService
from src.services.order_service import PedidoService
from src.repositories.product_repository import ProductRepository
from src.repositories.category_repository import CategoriaRepository
from src.repositories.order_repository import PedidoRepository
from src.repositories.user_repository import UsuarioRepository


class AdminController(BaseController):
    """
    Controller para operações administrativas.
    
    Métodos:
    - create_product(): Cria produto
    - update_product(): Atualiza produto
    - delete_product(): Deleta produto
    - list_all_orders(): Lista todos os pedidos
    - update_order_status(): Atualiza status do pedido
    - get_dashboard_stats(): Estatísticas do dashboard
    """
    
    def __init__(self, main_window):
        super().__init__(main_window)
        self.catalog_service = CatalogService()
        self.product_repo = ProductRepository()
        self.category_repo = CategoriaRepository()
        self.order_service = PedidoService(
            PedidoRepository(),
            ProductRepository(),
            UsuarioRepository()
        )
        self.current_admin_id = None
    
    def set_current_admin(self, admin_id: int) -> None:
        """
        Define o administrador atual.
        
        Args:
            admin_id: ID do administrador
        """
        self.current_admin_id = admin_id
    
    def create_product(
        self,
        nome: str,
        sku: str,
        preco: float,
        estoque: int,
        categoria_nome: str,
        descricao: str = ""
    ) -> Dict[str, Any]:
        """
        Cria novo produto.
        
        Args:
            nome: Nome do produto
            sku: SKU único
            preco: Preço
            estoque: Quantidade em estoque
            categoria_nome: Nome da categoria
            descricao: Descrição do produto
            
        Returns:
            Dicionário com success, message e data (produto)
        """
        if not self.current_admin_id:
            return self._error_response('Acesso negado')
        
        # Validações
        error = self._validate_not_empty(nome, "Nome")
        if error:
            return self._error_response(error)
        
        error = self._validate_not_empty(sku, "SKU")
        if error:
            return self._error_response(error)
        
        if preco <= 0:
            return self._error_response('Preço deve ser maior que zero')
        
        if estoque < 0:
            return self._error_response('Estoque não pode ser negativo')
        
        try:
            self.catalog_service.cadastrar_produto(
                nome=nome,
                sku=sku,
                preco=preco,
                estoque=estoque,
                nome_categoria=categoria_nome
            )
            
            return self._success_response('Produto criado com sucesso')
        
        except ValueError as e:
            return self._error_response(str(e))
        except Exception as e:
            return self._error_response('Erro ao criar produto', e)
    
    def update_product(
        self,
        produto_id: int,
        nome: Optional[str] = None,
        preco: Optional[float] = None,
        estoque: Optional[int] = None,
        descricao: Optional[str] = None,
        ativo: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Atualiza produto existente.
        
        Args:
            produto_id: ID do produto
            nome: Novo nome (opcional)
            preco: Novo preço (opcional)
            estoque: Novo estoque (opcional)
            descricao: Nova descrição (opcional)
            ativo: Novo status (opcional)
            
        Returns:
            Dicionário com success e message
        """
        if not self.current_admin_id:
            return self._error_response('Acesso negado')
        
        try:
            # Buscar produto atual
            produto = self.product_repo.buscar_por_id(produto_id)
            if not produto:
                return self._error_response('Produto não encontrado')
            
            # Atualizar campos fornecidos
            if nome is not None:
                produto['nome'] = nome
            if preco is not None:
                if preco <= 0:
                    return self._error_response('Preço inválido')
                produto['preco'] = preco
            if estoque is not None:
                if estoque < 0:
                    return self._error_response('Estoque inválido')
                produto['estoque'] = estoque
            if descricao is not None:
                produto['descricao'] = descricao
            if ativo is not None:
                produto['ativo'] = 1 if ativo else 0
            
            # Salvar
            self.product_repo.atualizar(produto)
            
            return self._success_response('Produto atualizado com sucesso')
        
        except Exception as e:
            return self._error_response('Erro ao atualizar produto', e)
    
    def delete_product(self, produto_id: int) -> Dict[str, Any]:
        """
        Deleta produto.
        
        Args:
            produto_id: ID do produto
            
        Returns:
            Dicionário com success e message
        """
        if not self.current_admin_id:
            return self._error_response('Acesso negado')
        
        try:
            resultado = self.catalog_service.remover_produto(produto_id)
            
            if resultado:
                return self._success_response('Produto deletado com sucesso')
            else:
                return self._error_response('Produto não encontrado')
        
        except Exception as e:
            return self._error_response('Erro ao deletar produto', e)
    
    def list_all_orders(
        self,
        status: Optional[str] = None,
        limit: int = 50
    ) -> Dict[str, Any]:
        """
        Lista todos os pedidos (admin).
        
        Args:
            status: Filtrar por status (opcional)
            limit: Limite de resultados
            
        Returns:
            Dicionário com success, message e data (pedidos)
        """
        if not self.current_admin_id:
            return self._error_response('Acesso negado')
        
        try:
            if status:
                pedidos = self.order_service.listar_por_status(
                    status,
                    limit=limit
                )
            else:
                pedidos = self.order_service.listar_todos_pedidos(
                    limit=limit
                )
            
            return self._success_response(
                f'{len(pedidos)} pedido(s) encontrado(s)',
                pedidos
            )
        
        except Exception as e:
            return self._error_response('Erro ao listar pedidos', e)
    
    def update_order_status(
        self,
        pedido_id: int,
        novo_status: str
    ) -> Dict[str, Any]:
        """
        Atualiza status de um pedido.
        
        Args:
            pedido_id: ID do pedido
            novo_status: Novo status
            
        Returns:
            Dicionário com success e message
        """
        if not self.current_admin_id:
            return self._error_response('Acesso negado')
        
        try:
            self.order_service.atualizar_status(pedido_id, novo_status)
            
            return self._success_response(
                f'Status do pedido #{pedido_id} atualizado'
            )
        
        except Exception as e:
            error_msg = str(e)
            
            if 'transição inválida' in error_msg.lower():
                return self._error_response(
                    'Transição de status não permitida'
                )
            else:
                return self._error_response(
                    'Erro ao atualizar status',
                    e
                )
    
    def get_dashboard_stats(self) -> Dict[str, Any]:
        """
        Obtém estatísticas para o dashboard admin.
        
        Returns:
            Dicionário com success, message e data (estatísticas)
        """
        if not self.current_admin_id:
            return self._error_response('Acesso negado')
        
        try:
            stats = {
                'total_produtos': len(self.catalog_service.listar_produtos()),
                'total_categorias': len(self.catalog_service.listar_categorias()),
                'pedidos_pendentes': self.order_service.contar_por_status('PENDENTE'),
                'pedidos_processando': self.order_service.contar_por_status('PROCESSANDO'),
                'pedidos_enviados': self.order_service.contar_por_status('ENVIADO'),
                'total_vendas': self.order_service.calcular_total_vendas()
            }
            
            return self._success_response(
                'Estatísticas carregadas',
                stats
            )
        
        except Exception as e:
            return self._error_response(
                'Erro ao carregar estatísticas',
                e
            )
    
    def navigate_to_products(self) -> None:
        """Navega para tela de gestão de produtos."""
        self.navigate_to('ManageProducts')
    
    def navigate_to_orders(self) -> None:
        """Navega para tela de gestão de pedidos."""
        result = self.list_all_orders()
        if result['success']:
            self.navigate_to('ManageOrders', result['data'])
    
    def navigate_to_dashboard(self) -> None:
        """Navega para dashboard admin."""
        self.navigate_to('AdminDashboard')
