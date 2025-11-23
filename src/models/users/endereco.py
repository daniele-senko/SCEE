from __future__ import annotations

from typing import Optional

from .base_model import BaseModel
from .users.client_model import Cliente


class Endereco(BaseModel):
    """
    Representa um endereço de entrega/faturamento de um cliente.
    """

    def __init__(
        self,
            cliente: Cliente,
            cep: str,
            rua: str,
            numero: str,
            bairro: str,
            cidade: str,
            estado: str,
            complemento: Optional[str] = None,
            padrao: bool = False,
            id: Optional[int] = None,
    ) -> None:
        self._id: Optional[int] = id
        self._cliente: Cliente | None = None
        self._cep: str | None = None
        self._rua: str | None = None
        self._numero: str | None = None
        self._bairro: str | None = None
        self._cidade: str | None = None
        self._estado: str | None = None
        self._complemento: str | None = None
        self._padrao: bool = bool(padrao)

        self.cliente = cliente
        self.cep = cep
        self.rua = rua
        self.numero = numero
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.complemento = complemento

    # --- ID / Cliente ---

    @property
    def id(self) -> Optional[int]:
        return self._id

    @property
    def cliente(self) -> Cliente:
        return self._cliente  # type: ignore[return-value]

    @cliente.setter
    def cliente(self, valor: Cliente) -> None:
        if not isinstance(valor, Cliente):
            raise TypeError("cliente deve ser uma instância de Cliente.")
        self._cliente = valor

    # --- CEP ---

    @property
    def cep(self) -> str:
        return self._cep  # type: ignore[return-value]

    @cep.setter
    def cep(self, valor: str) -> None:
        valor = (valor or "").strip()
        valor_num = "".join(filter(str.isdigit, valor))
        if len(valor_num) != 8:
            raise ValueError("CEP deve ter 8 dígitos.")
        self._cep = valor_num

    # --- Rua ---

    @property
    def rua(self) -> str:
        return self._rua  # type: ignore[return-value]

    @rua.setter
    def rua(self, valor: str) -> None:
        valor = (valor or "").strip()
        if len(valor) < 3:
            raise ValueError("Rua deve ter pelo menos 3 caracteres.")
        self._rua = valor

    # --- Número ---

    @property
    def numero(self) -> str:
        return self._numero  # type: ignore[return-value]

    @numero.setter
    def numero(self, valor: str) -> None:
        valor = (valor or "").strip()
        if not valor:
            raise ValueError("Número do endereço é obrigatório.")
        self._numero = valor

    # --- Bairro ---

    @property
    def bairro(self) -> str:
        return self._bairro  # type: ignore[return-value]

    @bairro.setter
    def bairro(self, valor: str) -> None:
        valor = (valor or "").strip()
        if len(valor) < 3:
            raise ValueError("Bairro deve ter pelo menos 3 caracteres.")
        self._bairro = valor

    # --- Cidade ---

    @property
    def cidade(self) -> str:
        return self._cidade  # type: ignore[return-value]

    @cidade.setter
    def cidade(self, valor: str) -> None:
        valor = (valor or "").strip()
        if len(valor) < 2:
            raise ValueError("Cidade deve ter pelo menos 2 caracteres.")
        self._cidade = valor

    # --- Estado (UF) ---

    @property
    def estado(self) -> str:
        return self._estado  # type: ignore[return-value]

    @estado.setter
    def estado(self, valor: str) -> None:
        valor = (valor or "").strip().upper()
        if len(valor) != 2:
            raise ValueError("Estado deve ser a sigla (UF), ex: 'MT', 'SP'.")
        self._estado = valor

    # --- Complemento / Padrão ---

    @property
    def complemento(self) -> Optional[str]:
        return self._complemento

    @complemento.setter
    def complemento(self, valor: Optional[str]) -> None:
        self._complemento = (valor or "").strip() or None

    @property
    def padrao(self) -> bool:
        return self._padrao

    @padrao.setter
    def padrao(self, valor: bool) -> None:
        self._padrao = bool(valor)

    # --- BaseModel ---

    def validar(self) -> None:
        """Valida consistência dos dados do endereço."""
        if self._cliente is None:
            raise ValueError("Endereço precisa estar associado a um cliente.")
        self._cliente.validar()

        # Reforça regras rodando setters
        self.cep = self._cep or ""
        self.rua = self._rua or ""
        self.numero = self._numero or ""
        self.bairro = self._bairro or ""
        self.cidade = self._cidade or ""
        self.estado = self._estado or ""

    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "cliente_id": self._cliente.id if self._cliente else None,
            "cep": self._cep,
            "rua": self._rua,
            "numero": self._numero,
            "bairro": self._bairro,
            "cidade": self._cidade,
            "estado": self._estado,
            "complemento": self._complemento,
            "padrao": self._padrao,
        }

    def __repr__(self) -> str:
        return (
            f"<Endereco {self._rua}, {self._numero} - "
            f"{self._bairro} - {self._cidade}/{self._estado}>"
        )
