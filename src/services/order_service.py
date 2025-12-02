"""Serviço de gerenciamento de pedidos."""

from typing import List, Dict, Any, Optional, Set
from decimal import Decimal
from datetime import datetime, timedelta
import logging

from src.repositories.order_repository import PedidoRepository
from src.repositories.product_repository import ProductRepository
from src.repositories.user_repository import UsuarioRepository


class PedidoServiceError(Exception):
    pass


class StatusInvalidoError(PedidoServiceError):
    pass


class TransicaoStatusInvalidaError(PedidoServiceError):
    pass


class PedidoNaoEncontradoError(PedidoServiceError):
    pass


class CancelamentoNaoPermitidoError(PedidoServiceError):
    pass


class PedidoService:
    """Serviço para gerenciamento de pedidos."""

    # Status válidos (Strings literais que batem com o banco)
    STATUS_PENDENTE = "PENDENTE"
    STATUS_PROCESSANDO = "PROCESSANDO"
    STATUS_ENVIADO = "ENVIADO"
    STATUS_ENTREGUE = "ENTREGUE"
    STATUS_CANCELADO = "CANCELADO"

    TODOS_STATUS = {
        STATUS_PENDENTE,
        STATUS_PROCESSANDO,
        STATUS_ENVIADO,
        STATUS_ENTREGUE,
        STATUS_CANCELADO,
    }

    TRANSICOES_VALIDAS = {
        STATUS_PENDENTE: {STATUS_PROCESSANDO, STATUS_CANCELADO},
        STATUS_PROCESSANDO: {STATUS_ENVIADO, STATUS_CANCELADO},
        STATUS_ENVIADO: {STATUS_ENTREGUE},
        STATUS_ENTREGUE: set(),
        STATUS_CANCELADO: set(),
    }

    TEMPO_LIMITE_CANCELAMENTO = 24  # horas

    def __init__(
        self,
        pedido_repo: PedidoRepository,
        produto_repo: ProductRepository,
        usuario_repo: UsuarioRepository,
    ):
        self.pedido_repo = pedido_repo
        self.produto_repo = produto_repo
        self.usuario_repo = usuario_repo

    def criar_pedido(
        self,
        usuario_id: int,
        endereco_id: int,
        itens: List[Dict[str, Any]],
        tipo_pagamento: str,
        frete: float = 0.0,
        observacoes: Optional[str] = None,
    ) -> Dict[str, Any]:
        if not itens:
            raise PedidoServiceError("Pedido deve conter pelo menos um item")

        # Calcular subtotal
        subtotal = Decimal("0.00")
        for item in itens:
            subtotal += Decimal(str(item["quantidade"])) * Decimal(
                str(item["preco_unitario"])
            )

        total = subtotal + Decimal(str(frete))

        try:
            pedido = self.pedido_repo.salvar(
                {
                    "usuario_id": usuario_id,
                    "endereco_id": endereco_id,
                    "subtotal": float(subtotal),
                    "frete": float(frete),
                    "total": float(total),
                    "status": self.STATUS_PENDENTE,
                    "tipo_pagamento": tipo_pagamento,
                    "observacoes": observacoes,
                }
            )

            # Adicionar itens
            for item in itens:
                prod = self.produto_repo.buscar_por_id(item["produto_id"])
                nome_prod = prod["nome"] if prod else "Produto"
                self.pedido_repo.adicionar_item(
                    pedido["id"],
                    item["produto_id"],
                    nome_prod,
                    item["quantidade"],
                    item["preco_unitario"],
                )

            return pedido
        except Exception as e:
            raise PedidoServiceError(f"Erro ao criar pedido: {str(e)}")

    def buscar_por_id(
        self, pedido_id: int, completo: bool = False
    ) -> Optional[Dict[str, Any]]:
        if completo:
            return self.pedido_repo.buscar_completo(pedido_id)
        return self.pedido_repo.buscar_por_id(pedido_id)

    def listar_pedidos_usuario(self, usuario_id: int) -> List[Dict[str, Any]]:
        return self.pedido_repo.listar_por_usuario(usuario_id)

    def atualizar_status(self, pedido_id: int, novo_status: str) -> bool:
        self._validar_status(novo_status)
        pedido = self.pedido_repo.buscar_por_id(pedido_id)
        if not pedido:
            raise PedidoNaoEncontradoError("Pedido não encontrado")
        return self.pedido_repo.atualizar_status(pedido_id, novo_status)

    def cancelar_pedido(
        self,
        pedido_id: int,
        usuario_id: Optional[int] = None,
        motivo: Optional[str] = None,
    ) -> bool:
        pedido = self.pedido_repo.buscar_completo(pedido_id)
        if not pedido:
            raise PedidoNaoEncontradoError("Pedido não encontrado")

        if usuario_id and pedido["usuario_id"] != usuario_id:
            raise CancelamentoNaoPermitidoError("Pedido pertence a outro usuário")

        if not self._pode_cancelar(pedido):
            raise CancelamentoNaoPermitidoError(
                "Cancelamento não permitido (status ou prazo inválido)"
            )

        # Atualiza status
        obs = pedido.get("observacoes", "") or ""
        if motivo:
            obs += f"\n[CANCELADO]: {motivo}"

        pedido["status"] = self.STATUS_CANCELADO
        pedido["observacoes"] = obs

        # Chama repositório para atualizar status (Trigger do banco devolve estoque)
        self.pedido_repo.atualizar_status(pedido["id"], self.STATUS_CANCELADO)

        return True

    def obter_historico_completo(self, pedido_id: int) -> Dict[str, Any]:
        pedido = self.pedido_repo.buscar_completo(pedido_id)
        if not pedido:
            raise PedidoNaoEncontradoError("Pedido não encontrado")

        # Injeta flags de regra de negócio
        pedido["pode_cancelar"] = self._pode_cancelar(pedido)

        return pedido

    # --- Validações ---

    def _validar_status(self, status: str):
        if status not in self.TODOS_STATUS:
            raise StatusInvalidoError(f"Status inválido: {status}")

    def _pode_cancelar(self, pedido: Dict[str, Any]) -> bool:
        """Verifica se o pedido pode ser cancelado (Debug Version)."""
        status = pedido.get("status")
        print(f"DEBUG CANCELAR: Status do pedido #{pedido.get('id')} é '{status}'")

        # 1. Regra de Status
        if status not in {self.STATUS_PENDENTE, self.STATUS_PROCESSANDO}:
            print(
                f"DEBUG CANCELAR: Bloqueado por status (esperado PENDENTE ou PROCESSANDO)"
            )
            return False

        # 2. Regra de Tempo (24h)
        criado_em_raw = pedido.get("criado_em")
        print(f"DEBUG CANCELAR: Data bruta '{criado_em_raw}'")

        if not criado_em_raw:
            return True  # Se não tiver data, libera na dúvida

        try:
            # Tenta formatos comuns do SQLite
            if isinstance(criado_em_raw, datetime):
                criado_em = criado_em_raw
            elif "." in str(criado_em_raw):
                # Formato com milissegundos: "2023-11-30 12:00:00.123456"
                criado_em = datetime.strptime(
                    str(criado_em_raw).split(".")[0], "%Y-%m-%d %H:%M:%S"
                )
            else:
                # Formato padrão: "2023-11-30 12:00:00"
                criado_em = datetime.strptime(str(criado_em_raw), "%Y-%m-%d %H:%M:%S")

            tempo_decorrido = datetime.now() - criado_em
            horas_passadas = tempo_decorrido.total_seconds() / 3600

            print(f"DEBUG CANCELAR: Passaram-se {horas_passadas:.2f} horas")

            if tempo_decorrido > timedelta(hours=self.TEMPO_LIMITE_CANCELAMENTO):
                print("DEBUG CANCELAR: Bloqueado por tempo (> 24h)")
                return False

        except Exception as e:
            print(f"DEBUG CANCELAR: Erro ao processar data: {e}")
            # Em caso de erro de parse, permite cancelar (fail-safe)
            return True

        return True
