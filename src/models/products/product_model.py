from __future__ import annotations
from typing import Optional

from ..base_model import BaseModel
from .category_model import Categoria
from src.utils.validators.price_validator import PriceValidator



class Produto(BaseModel):
    """
    Representa um item físico vendável no sistema.
    Possui relacionamento com Categoria e validações financeiras.
    """

    def __init__(
        self,
        nome: str,
        sku: str,
        preco: float,
        categoria: Categoria,
        estoque: int = 0,
        id: Optional[int] = None,
    ):
        """
        :param nome: Título do produto
        :param sku: Código único (Stock Keeping Unit)
        :param preco: Valor unitário (validado)
        :param categoria: Objeto da classe Categoria (Agregação)
        :param estoque: Quantidade inicial (validado)
        """
        self._id: Optional[int] = id
        self._nome: str | None = None
        self._sku: str | None = None
        self._categoria: Categoria | None = None
        self._preco: float = 0.0
        self._estoque: int = 0

        # Setters com validação
        self.nome = nome
        self.sku = sku
        self.categoria = categoria
        self.preco = preco
        self.estoque = estoque

    @property
    def id(self) -> Optional[int]:
        return self._id

    # --- Nome ---

    @property
    def nome(self) -> str:
        return self._nome  # type: ignore[return-value]

    @nome.setter
    def nome(self, valor: str) -> None:
        valor = (valor or "").strip()
        if len(valor) < 3:
            raise ValueError("Nome do produto deve ter pelo menos 3 caracteres.")
        self._nome = valor

    # --- SKU ---

    @property
    def sku(self) -> str:
        return self._sku  # type: ignore[return-value]

    @sku.setter
    def sku(self, valor: str) -> None:
        valor = (valor or "").strip().upper()
        if len(valor) < 3:
            raise ValueError("SKU deve ter pelo menos 3 caracteres.")
        self._sku = valor

    # --- Categoria ---

    @property
    def categoria(self) -> Categoria:
        return self._categoria  # type: ignore[return-value]

    @categoria.setter
    def categoria(self, valor: Categoria) -> None:
        if not isinstance(valor, Categoria):
            raise TypeError("categoria deve ser uma instância de Categoria.")
        self._categoria = valor

    # --- Preço ---

    @property
    def preco(self) -> float:
        return self._preco

    @preco.setter
    def preco(self, valor: float) -> None:
        # Validação usando a classe utilitária
        if not PriceValidator.validate_price(valor):
            raise ValueError(f"Preço inválido para o produto '{self.nome}': {valor}")
        self._preco = float(valor)

    # --- Estoque ---

    @property
    def estoque(self) -> int:
        return self._estoque

    @estoque.setter
    def estoque(self, valor: int) -> None:
        if not PriceValidator.validate_stock(valor):
            raise ValueError(f"Estoque inválido: {valor}")
        self._estoque = int(valor)

    # --- Métodos auxiliares ---

    def tem_estoque(self, quantidade: int = 1) -> bool:
        """Verifica se há quantidade suficiente para venda."""
        return self.estoque >= quantidade

    # --- BaseModel ---

    def validar(self) -> None:
        if not self._nome or len(self._nome) < 3:
            raise ValueError("Produto sem nome válido.")
        if not self._sku:
            raise ValueError("Produto sem SKU.")
        if not isinstance(self._categoria, Categoria):
            raise ValueError("Categoria inválida para o produto.")
        # reutiliza os setters
        self.preco = self._preco
        self.estoque = self._estoque
        self._categoria.validar()

    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "nome": self._nome,
            "sku": self._sku,
            "preco": self._preco,
            "estoque": self._estoque,
            "categoria_id": self._categoria.id if self._categoria else None,
            "categoria_nome": self._categoria.nome if self._categoria else None,
        }

    def __str__(self) -> str:
        return f"{self.nome} - R$ {self.preco:.2f}"
