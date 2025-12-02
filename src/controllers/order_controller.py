"""
OrderController - Controlador de Pedidos
========================================

Gerencia criação e consulta de pedidos.
"""

from typing import Dict, Any, List
from src.controllers.base_controller import BaseController
from src.services.order_service import PedidoService, CancelamentoNaoPermitidoError
from src.repositories.order_repository import PedidoRepository
from src.repositories.product_repository import ProductRepository
from src.repositories.user_repository import UsuarioRepository


class OrderController(BaseController):
    """
    Controller para operações de pedidos.
    """

    def __init__(self, main_window):
        super().__init__(main_window)
        self.order_service = PedidoService(
            PedidoRepository(), ProductRepository(), UsuarioRepository()
        )
        self.current_usuario_id = None

    def set_current_user(self, usuario_id: int) -> None:
        self.current_usuario_id = usuario_id

    def create_order(
        self,
        endereco_id: int,
        itens: List[Dict[str, Any]],
        tipo_pagamento: str,
        frete: float = 0.0,
        observacoes: str = None,
    ) -> Dict[str, Any]:
        if not self.current_usuario_id:
            return self._error_response("Usuário não autenticado")

        if not itens:
            return self._error_response("Pedido deve ter pelo menos um item")

        try:
            pedido = self.order_service.criar_pedido(
                usuario_id=self.current_usuario_id,
                endereco_id=endereco_id,
                itens=itens,
                tipo_pagamento=tipo_pagamento,
                frete=frete,
                observacoes=observacoes,
            )

            return self._success_response(
                f'Pedido #{pedido["id"]} criado com sucesso!', pedido
            )

        except Exception as e:
            return self._error_response("Erro ao criar pedido", e)

    def list_my_orders(self) -> Dict[str, Any]:
        """Lista os pedidos do usuário logado."""
        if not self.current_usuario_id:
            return self._error_response("Usuário não autenticado")

        try:
            # Chama o repositório diretamente para leitura (mais eficiente)
            # ou o service se tiver regras de negócio (ex: formatação)
            pedidos = self.order_service.listar_pedidos_usuario(self.current_usuario_id)

            # Formata ou enriquece os dados se necessário
            for p in pedidos:
                p["total"] = float(p["total"])
            return self._success_response(
                f"{len(pedidos)} pedidos encontrados", pedidos
            )

        except Exception as e:
            return self._error_response("Erro ao listar pedidos", e)

    def get_order_details(self, pedido_id: int) -> Dict[str, Any]:
        """
        Obtém detalhes completos de um pedido.
        """
        if not self.current_usuario_id:
            return self._error_response("Usuário não autenticado")

        try:
            pedido = self.order_service.obter_historico_completo(pedido_id)

            if not pedido:
                return self._error_response("Pedido não encontrado")

            # Verificar se o pedido pertence ao usuário
            if pedido["usuario_id"] != self.current_usuario_id:
                return self._error_response("Acesso negado")

            return self._success_response("Pedido encontrado", pedido)

        except Exception as e:
            return self._error_response("Erro ao buscar pedido", e)

        except Exception as e:
            return self._error_response("Erro ao buscar pedido", e)

    def cancel_order(self, pedido_id: int) -> Dict[str, Any]:
        """Solicita o cancelamento de um pedido."""
        if not self.current_usuario_id:
            return self._error_response("Usuário não autenticado")

        try:
            # Chama o serviço passando o ID do usuário para garantir que ele é o dono
            self.order_service.cancelar_pedido(
                pedido_id,
                usuario_id=self.current_usuario_id,
                motivo="Cancelado pelo cliente via Portal",
            )
            return self._success_response("Pedido cancelado com sucesso!")

        except CancelamentoNaoPermitidoError as e:
            return self._error_response(str(e))
        except Exception as e:
            return self._error_response("Erro ao cancelar pedido", e)
