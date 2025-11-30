from abc import ABC, abstractmethod
from typing import Dict, Any
from src.models.enums import StatusPagamento

class PaymentGateway(ABC):
    """Interface base para gateways de pagamento."""
    
    @abstractmethod
    def processar_pagamento(self, valor: float, dados: Dict[str, Any]) -> StatusPagamento:
        pass