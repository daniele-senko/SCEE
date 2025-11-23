from __future__ import annotations
from typing import Optional

from ..base_model import BaseModel
from src.utils.validators.email_validator import EmailValidator


class Usuario(BaseModel):
    """
    Classe Base que representa um usuário genérico do sistema.
    Deve ser herdada por Cliente e Administrador.
    """

    def __init__(self, nome: str, email: str, senha_hash: str, id: Optional[int] = None):
        """
        :param nome: Nome completo
        :param email: E-mail para login
        :param senha_hash: Senha já criptografada
        :param id: ID do banco de dados (opcional na criação)
        """
        self._id: Optional[int] = id
        self._nome: str | None = None
        self._email: str | None = None
        self._senha_hash: str | None = None

        # Usa setters (com validação)
        self.nome = nome
        self.email = email
        self.senha_hash = senha_hash

    # --- ID (somente leitura) ---

    @property
    def id(self) -> Optional[int]:
        """ID do usuário (somente leitura)."""
        return self._id

    # --- Nome ---

    @property
    def nome(self) -> str:
        return self._nome  # type: ignore[return-value]

    @nome.setter
    def nome(self, valor: str) -> None:
        valor = (valor or "").strip()
        if len(valor) < 3:
            raise ValueError("Nome deve ter pelo menos 3 caracteres.")
        self._nome = valor

    # --- Email ---

    @property
    def email(self) -> str:
        return self._email  # type: ignore[return-value]

    @email.setter
    def email(self, valor: str) -> None:
        """
        Setter para o e-mail com validação.
        Lança erro se o formato for inválido.
        """
        if not EmailValidator.validate(valor):
            raise ValueError(f"E-mail inválido: {valor}")
        self._email = valor

    # --- Senha hash ---

    @property
    def senha_hash(self) -> str:
        return self._senha_hash  # type: ignore[return-value]

    @senha_hash.setter
    def senha_hash(self, valor: str) -> None:
        valor = (valor or "").strip()
        if len(valor) == 0:
            raise ValueError("Hash de senha não pode ser vazio.")
        self._senha_hash = valor

    # --- Métodos do BaseModel ---

    def validar(self) -> None:
        """Valida dados básicos do usuário."""
        if not self._nome or len(self._nome) < 3:
            raise ValueError("Nome inválido.")
        if not self._email or not EmailValidator.validate(self._email):
            raise ValueError("E-mail inválido.")
        if not self._senha_hash:
            raise ValueError("Senha hash obrigatória.")

    def to_dict(self) -> dict:
        """Representação serializável do usuário."""
        return {
            "id": self._id,
            "nome": self._nome,
            "email": self._email,
        }

    def __str__(self) -> str:
        return f"{self.nome} ({self.email})"
