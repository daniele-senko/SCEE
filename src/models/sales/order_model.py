from __future__ import annotations
from typing import List, Optional, Dict, Any
from datetime import datetime

from src.models.base_model import BaseModel
from src.models.sales.cart_item_model import ItemPedido
from src.models.enums import StatusPedido

class Pedido(BaseModel):
    """
    Representa um Pedido de Venda no sistema.
    Agrega informações do cliente, itens, valores e status.
    """

    def __init__(
        self,
        cliente_id: int,
        valor_total: float,
        itens: List[ItemPedido],
        endereco_entrega_id: int,
        tipo_pagamento: str, 
        status: str = StatusPedido.PAGAMENTO_PENDENTE,
        frete: float = 0.0,
        id: Optional[int] = None,
        data_pedido: Optional[datetime] = None
    ) -> None:
        self._id: Optional[int] = id
        self._cliente_id: int = cliente_id
        self._endereco_entrega_id: int = endereco_entrega_id
        self._tipo_pagamento: str = tipo_pagamento
        self._status: str = status
        self._itens: List[ItemPedido] = itens
        self._frete: float = float(frete)
        self._valor_total: float = float(valor_total)
        self._data_pedido: datetime = data_pedido or datetime.now()

        if not self._itens:
            raise ValueError("Um pedido deve ter pelo menos um item.")
        if self._valor_total < 0:
            raise ValueError("O valor total do pedido não pode ser negativo.")

    # --- Properties (Getters/Setters) ---

    @property
    def id(self) -> Optional[int]:
        return self._id
    
    @property
    def tipo_pagamento(self) -> str:
        return self._tipo_pagamento

    @id.setter
    def id(self, valor: int) -> None:
        self._id = valor

    @property
    def cliente_id(self) -> int:
        return self._cliente_id

    @property
    def endereco_entrega_id(self) -> int:
        return self._endereco_entrega_id

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, novo_status: str) -> None:
        self._status = novo_status

    @property
    def itens(self) -> List[ItemPedido]:
        return self._itens

    @property
    def frete(self) -> float:
        return self._frete

    @property
    def valor_total(self) -> float:
        return self._valor_total

    @property
    def subtotal(self) -> float:
        """
        Calcula o subtotal somando os itens (sem frete).
        """
        return sum(item.total_liquido for item in self._itens)

    @property
    def total_itens(self) -> int:
        """Retorna a quantidade total de produtos no pedido."""
        return sum(item.quantidade for item in self._itens)

    # --- Métodos do BaseModel ---

    def validar(self) -> None:
        """Valida a integridade do pedido."""
        if self._cliente_id <= 0:
            raise ValueError("Pedido deve ter um cliente válido.")
        if not self._itens:
            raise ValueError("Pedido vazio.")
        # Valida cada item individualmente
        for item in self._itens:
            item.validar()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self._id,
            "cliente_id": self._cliente_id,
            "endereco_entrega_id": self._endereco_entrega_id,
            "tipo_pagamento": self._tipo_pagamento,
            "status": self._status,
            "frete": self._frete,
            "subtotal": self.subtotal,
            "valor_total": self._valor_total,
            "data_pedido": self._data_pedido.isoformat() if self._data_pedido else None,
            "itens": [item.to_dict() for item in self._itens]
        }

    def __str__(self) -> str:
        return f"Pedido #{self._id or '?'} - Total: R$ {self._valor_total:.2f} ({self.status})"