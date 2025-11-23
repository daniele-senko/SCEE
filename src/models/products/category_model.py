from __future__ import annotations
from typing import Optional

from ..base_model import BaseModel



class Categoria(BaseModel):
    """
    Representa uma categoria de produtos na loja (ex: Hardware, Periféricos).
    Serve para agrupar e filtrar produtos.
    """

    def __init__(self, nome: str, id: Optional[int] = None):
        """
        :param nome: Nome da categoria (ex: 'Placas de Vídeo')
        :param id: Identificador único do banco (opcional na criação)
        """
        self._id: Optional[int] = id
        self._nome: str | None = None
        self.nome = nome

    @property
    def id(self) -> Optional[int]:
        """Getter do ID (somente leitura)."""
        return self._id

    @property
    def nome(self) -> str:
        return self._nome  # type: ignore[return-value]

    @nome.setter
    def nome(self, valor: str) -> None:
        valor = (valor or "").strip()
        if len(valor) < 3:
            raise ValueError("Nome da categoria deve ter pelo menos 3 caracteres.")
        self._nome = valor

    # --- BaseModel ---

    def validar(self) -> None:
        if not self._nome or len(self._nome) < 3:
            raise ValueError("Categoria inválida.")

    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "nome": self._nome,
        }

    def __str__(self) -> str:
        return self.nome

    def __repr__(self) -> str:
        return f"<Categoria: {self.nome} (ID: {self._id})>"
