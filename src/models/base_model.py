from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseModel(ABC):
    """
    Classe base abstrata para todos os modelos de domínio.
    Garante que todo model tenha validar() e to_dict().
    """

    @abstractmethod
    def validar(self) -> None:
        """Dispara ValueError se o objeto estiver inválido."""
        raise NotImplementedError

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Retorna representação serializável do objeto."""
        raise NotImplementedError