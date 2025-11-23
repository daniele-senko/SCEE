from __future__ import annotations

from typing import Optional

from src.models.users.user_model import Usuario


class Administrador(Usuario):
    """
    Representa um usuário administrativo com permissões de gestão.
    """

    def __init__(
        self,
        nome: str,
        email: str,
        senha_hash: str,
        nivel_acesso: str = "padrao",
        id: Optional[int] = None,
    ):
        super().__init__(nome, email, senha_hash, id)
        self._nivel_acesso: str | None = None
        self.nivel_acesso = nivel_acesso  # ex: 'gerente', 'estoquista'

    @property
    def nivel_acesso(self) -> str:
        return self._nivel_acesso  # type: ignore[return-value]

    @nivel_acesso.setter
    def nivel_acesso(self, valor: str) -> None:
        valor = (valor or "").strip().lower()
        if valor not in {"padrao", "gerente", "estoquista", "admin"}:
            raise ValueError("Nível de acesso inválido.")
        self._nivel_acesso = valor

    def tem_permissao_gerencial(self) -> bool:
        """Verifica se o admin é um gerente."""
        return self.nivel_acesso == "gerente"

    # --- BaseModel overrides ---

    def validar(self) -> None:
        super().validar()
        if not self._nivel_acesso:
            raise ValueError("Nível de acesso obrigatório.")

    def to_dict(self) -> dict:
        base = super().to_dict()
        base.update(
            {
                "nivel_acesso": self._nivel_acesso,
            }
        )
        return base

    def __repr__(self) -> str:
        return f"<Admin: {self.nome} - Nível: {self.nivel_acesso}>"
