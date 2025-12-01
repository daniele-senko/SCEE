from __future__ import annotations
from typing import Optional
from src.models.base_model import BaseModel
from src.models.products.category_model import Categoria
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
        descricao: str = "",
        imagem_principal: Optional[
            str
        ] = None,
        id: Optional[int] = None,
    ):
        self._id: Optional[int] = id
        self._nome: str | None = None
        self._sku: str | None = None
        self._categoria: Categoria | None = None
        self._preco: float = 0.0
        self._estoque: int = 0
        self._descricao: str = ""
        self._imagem_principal: str | None = None

        # Setters com validação
        self.nome = nome
        self.sku = sku
        self.categoria = categoria
        self.preco = preco
        self.estoque = estoque
        self.descricao = descricao
        self.imagem_principal = imagem_principal

    @property
    def id(self) -> Optional[int]:
        return self._id

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, valor: str) -> None:
        valor = (valor or "").strip()
        if len(valor) < 3:
            raise ValueError("Nome do produto deve ter pelo menos 3 caracteres.")
        self._nome = valor

    @property
    def sku(self) -> str:
        return self._sku

    @sku.setter
    def sku(self, valor: str) -> None:
        valor = (valor or "").strip().upper()
        if len(valor) < 3:
            raise ValueError("SKU deve ter pelo menos 3 caracteres.")
        self._sku = valor

    @property
    def categoria(self) -> Categoria:
        return self._categoria

    @categoria.setter
    def categoria(self, valor: Categoria) -> None:
        if not isinstance(valor, Categoria):
            raise TypeError("categoria deve ser uma instância de Categoria.")
        self._categoria = valor

    @property
    def preco(self) -> float:
        return self._preco

    @preco.setter
    def preco(self, valor: float) -> None:
        if not PriceValidator.validate_price(valor):
            raise ValueError(f"Preço inválido: {valor}")
        self._preco = float(valor)

    @property
    def estoque(self) -> int:
        return self._estoque

    @estoque.setter
    def estoque(self, valor: int) -> None:
        if not PriceValidator.validate_stock(valor):
            raise ValueError(f"Estoque inválido: {valor}")
        self._estoque = int(valor)

    @property
    def descricao(self) -> str:
        return self._descricao

    @descricao.setter
    def descricao(self, valor: str) -> None:
        # Garante que nunca seja None, evita erro na interface
        self._descricao = (valor or "").strip()

    @property
    def imagem_principal(self) -> Optional[str]:
        return self._imagem_principal

    @imagem_principal.setter
    def imagem_principal(self, valor: Optional[str]) -> None:
        self._imagem_principal = valor

    # --- Métodos auxiliares ---

    def tem_estoque(self, quantidade: int = 1) -> bool:
        return self.estoque >= quantidade

    def validar(self) -> None:
        if not self._nome or len(self._nome) < 3:
            raise ValueError("Produto sem nome válido.")
        if not self._sku:
            raise ValueError("Produto sem SKU.")
        if not isinstance(self._categoria, Categoria):
            raise ValueError("Categoria inválida.")

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
            "descricao": self._descricao,
            "imagem_principal": self._imagem_principal,
            "categoria_id": self._categoria.id if self._categoria else None,
            "categoria_nome": self._categoria.nome if self._categoria else None,
        }

    def __str__(self) -> str:
        return f"{self.nome} - R$ {self.preco:.2f}"
