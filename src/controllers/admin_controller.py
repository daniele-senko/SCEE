"""
AdminController - Controlador do Administrador
"""
from typing import Dict, Any
from src.controllers.base_controller import BaseController
from src.repositories.product_repository import ProductRepository
from src.repositories.order_repository import PedidoRepository
from src.repositories.category_repository import CategoryRepository

class AdminController(BaseController):
    
    def __init__(self, main_window):
        super().__init__(main_window)
        self.product_repo = ProductRepository()
        self.order_repo = PedidoRepository()
        self.category_repo = CategoryRepository()
        self.current_admin_id = None

    def set_current_admin(self, admin_id: int) -> None:
        self.current_admin_id = admin_id

    # --- DASHBOARD ---
    def get_dashboard_stats(self) -> Dict[str, Any]:
        try:
            total_vendas = self.order_repo.calcular_total_vendas()
            pendentes = self.order_repo.contar_por_status('PROCESSANDO')
            todos_produtos = self.product_repo.listar()
            qtd_produtos = len(todos_produtos)

            stats = {
                'total_vendas': total_vendas,
                'pedidos_pendentes': pendentes,
                'total_produtos': qtd_produtos
            }
            return self._success_response('Stats recuperados', stats)
        except Exception as e:
            return self._error_response('Erro ao carregar dashboard', e)

    # --- PEDIDOS ---
    def list_all_orders(self, status: str = None, limit: int = 50) -> Dict[str, Any]:
        try:
            # O repositório agora retorna dados da VIEW (com cliente_nome)
            if status:
                pedidos = self.order_repo.listar_por_status(status, limit=limit)
            else:
                pedidos = self.order_repo.listar(limit=limit)
            
            for pedido in pedidos:
                if 'itens' not in pedido:
                    pedido['itens'] = self.order_repo.listar_itens(pedido['id'])
            
            return self._success_response('Pedidos listados', pedidos)
        except Exception as e:
            return self._error_response('Erro ao listar pedidos', e)

    def update_order_status(self, pedido_id: int, novo_status: str) -> Dict[str, Any]:
        try:
            self.order_repo.atualizar_status(pedido_id, novo_status)
            return self._success_response(f'Status atualizado para {novo_status}')
        except Exception as e:
            return self._error_response('Erro ao atualizar status', e)

    # --- CATEGORIAS ---
    
    def list_all_categories(self) -> Dict[str, Any]:
        try:
            categorias = self.category_repo.listar()
            return self._success_response('Categorias recuperadas', categorias)
        except Exception as e:
            return self._error_response('Erro ao listar categorias', e)

    def add_category(self, nome: str, descricao: str) -> Dict[str, Any]:
        if not nome: return self._error_response("Nome é obrigatório")
        try:
            existente = self.category_repo.buscar_por_nome(nome)
            if existente: return self._error_response(f"Categoria '{nome}' já existe.")
            nova_cat = {'nome': nome, 'descricao': descricao, 'ativo': 1}
            self.category_repo.salvar(nova_cat)
            return self._success_response('Categoria cadastrada com sucesso!')
        except Exception as e:
            return self._error_response('Erro ao salvar categoria', e)

    def update_category(self, categoria_id: int, nome: str, descricao: str) -> Dict[str, Any]:
        try:
            existente = self.category_repo.buscar_por_nome(nome)
            if existente and existente['id'] != categoria_id:
                return self._error_response(f"Já existe outra categoria com o nome '{nome}'.")
            dados = {'id': categoria_id, 'nome': nome, 'descricao': descricao, 'ativo': 1}
            self.category_repo.atualizar(dados)
            return self._success_response('Categoria atualizada com sucesso!')
        except Exception as e:
            return self._error_response('Erro ao atualizar categoria', e)

    def toggle_category(self, categoria_id: int, novo_status_bool: bool) -> Dict[str, Any]:
        try:
            cat = self.category_repo.buscar_por_id(categoria_id)
            if not cat: return self._error_response('Categoria não encontrada')
            cat['ativo'] = 1 if novo_status_bool else 0
            self.category_repo.atualizar(cat)
            status_str = "ativada" if novo_status_bool else "desativada"
            return self._success_response(f'Categoria {status_str} com sucesso!')
        except Exception as e:
            return self._error_response('Erro ao alterar status', e)