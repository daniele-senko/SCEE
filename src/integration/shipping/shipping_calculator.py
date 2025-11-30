from abc import ABC, abstractmethod

class ShippingCalculator(ABC):
    """Interface (Strategy) para cálculo de frete."""
    
    @abstractmethod
    def calcular(self, cep_destino: str, peso_total: float) -> float:
        pass