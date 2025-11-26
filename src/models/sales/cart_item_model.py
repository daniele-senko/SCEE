from __future__ import annotations

from typing import Optional

from ..base_model import BaseModel
from ..products.product_model import Produto
from src.utils.validators.price_validator import PriceValidator


class ItemPedido(BaseModel):
    """
    Representa uma linha do pedido (um produto + quantidade + preço).
    É o elo entre Pedido e Produto.
    """

    def __init__(
        self,
        produto: Produto,
        quantidade: int,
        preco_unitario: Optional[float] = None,
        desconto: float = 0.0,
        id: Optional[int] = None,
        pedido_id: Optional[int] = None,
    ) -> None:
        """
        :param produto: Objeto Produto associado
        :param quantidade: Quantidade do produto neste item
        :param preco_unitario: Preço unitário no momento da venda
                               (se None, usa produto.preco)
        :param desconto: Desconto em valor absoluto (R$) neste item
        :param id: ID do item no banco de dados
        :param pedido_id: FK opcional para o Pedido
        """
        self._id: Optional[int] = id
        self._pedido_id: Optional[int] = pedido_id
        self._produto: Produto | None = None
        self._quantidade: int = 0
        self._preco_unitario: float = 0.0
        self._desconto: float = 0.0

        # usa setters (com validação)
        self.produto = produto
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario if preco_unitario is not None else produto.preco
        self.desconto = desconto

    # --- ID / Pedido ---

    @property
    def id(self) -> Optional[int]:
        return self._id

    @property
    def pedido_id(self) -> Optional[int]:
        """FK do pedido ao qual o item pertence."""
        return self._pedido_id

    @pedido_id.setter
    def pedido_id(self, valor: Optional[int]) -> None:
        if valor is not None and valor <= 0:
            raise ValueError("pedido_id deve ser positivo.")
        self._pedido_id = valor

    # --- Produto ---

    @property
    def produto(self) -> Produto:
        return self._produto  # type: ignore[return-value]

    @produto.setter
    def produto(self, valor: Produto) -> None:
        if not isinstance(valor, Produto):
            raise TypeError("produto deve ser uma instância de Produto.")
        self._produto = valor

    # --- Quantidade ---

    @property
    def quantidade(self) -> int:
        return self._quantidade

    @quantidade.setter
    def quantidade(self, valor: int) -> None:
        if not isinstance(valor, int):
            raise TypeError("quantidade deve ser inteiro.")
        if valor <= 0:
            raise ValueError("quantidade deve ser maior que zero.")
        # podemos reutilizar validação de estoque se quiser
        if not PriceValidator.validate_stock(valor):
            raise ValueError(f"Quantidade inválida: {valor}")
        self._quantidade = valor

    # --- Preço unitário ---

    @property
    def preco_unitario(self) -> float:
        return self._preco_unitario

    @preco_unitario.setter
    def preco_unitario(self, valor: float) -> None:
        if not PriceValidator.validate_price(valor):
            raise ValueError(f"Preço unitário inválido: {valor}")
        self._preco_unitario = float(valor)

    # --- Desconto (valor em R$) ---

    @property
    def desconto(self) -> float:
        return self._desconto

    @desconto.setter
    def desconto(self, valor: float) -> None:
        if valor < 0:
            raise ValueError("Desconto não pode ser negativo.")
        # não deixa desconto maior que o total bruto
        total_bruto = self._preco_unitario * self._quantidade
        if valor > total_bruto:
            raise ValueError("Desconto não pode ser maior que o total do item.")
        self._desconto = float(valor)

    # --- Cálculos ---

    @property
    def total_bruto(self) -> float:
        """preco_unitario * quantidade (sem desconto)."""
        return self._preco_unitario * self._quantidade

    @property
    def total_liquido(self) -> float:
        """Total do item já considerando desconto."""
        return max(self.total_bruto - self._desconto, 0.0)

    # --- BaseModel ---

    def validar(self) -> None:
        """Valida consistência do ItemPedido."""
        if self._produto is None:
            raise ValueError("ItemPedido deve ter um produto associado.")
        self._produto.validar()

        # Reaproveita setters para garantir regras
        self.quantidade = self._quantidade
        self.preco_unitario = self._preco_unitario
        self.desconto = self._desconto

    def to_dict(self) -> dict:
        """Representação serializável do item."""
        return {
            "id": self._id,
            "pedido_id": self._pedido_id,
            "produto_id": self._produto.id if self._produto else None,
            "produto_nome": self._produto.nome if self._produto else None,
            "sku": self._produto.sku if self._produto else None,
            "quantidade": self._quantidade,
            "preco_unitario": self._preco_unitario,
            "desconto": self._desconto,
            "total_bruto": self.total_bruto,
            "total_liquido": self.total_liquido,
        }

    def __repr__(self) -> str:
        return (
            f"<ItemPedido produto={self._produto.nome if self._produto else None} "
            f"qtd={self._quantidade} total={self.total_liquido:.2f}>"
        )
