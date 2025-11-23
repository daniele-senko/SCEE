from __future__ import annotations

from typing import Optional

from src.models.users.user_model import Usuario
from src.utils.validators.cpf_validator import CpfValidator


class Cliente(Usuario):
    """
    Representa o cliente da loja.
    Herda atributos e métodos da classe Usuario.
    """

    def __init__(self, nome: str, email: str, cpf: str, senha_hash: str, id: Optional[int] = None):
        # Chama o construtor da classe pai (Usuario) para configurar nome, email, senha
        super().__init__(nome, email, senha_hash, id)

        self._cpf: str | None = None
        self.cpf = cpf  # Usa o setter para validar

    @property
    def cpf(self) -> str:
        return self._cpf  # type: ignore[return-value]

    @cpf.setter
    def cpf(self, valor: str) -> None:
        if not CpfValidator.validate(valor):
            raise ValueError(f"CPF inválido: {valor}")
        self._cpf = valor

    # --- Sobrescrita do validar/to_dict para incluir CPF ---

    def validar(self) -> None:
        """Valida os dados do cliente (incluindo CPF)."""
        super().validar()
        if not self._cpf or not CpfValidator.validate(self._cpf):
            raise ValueError("CPF inválido para cliente.")

    def to_dict(self) -> dict:
        base = super().to_dict()
        base.update(
            {
                "cpf": self._cpf,
            }
        )
        return base

    def __repr__(self) -> str:
        return f"<Cliente: {self.nome} - CPF: {self.cpf}>"
