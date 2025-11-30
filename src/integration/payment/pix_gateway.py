from typing import Dict, Any
from src.models.enums import StatusPagamento
from .payment_gateway import PaymentGateway

class PixGateway(PaymentGateway):
    def processar_pagamento(self, valor: float, dados: Dict[str, Any]) -> StatusPagamento:
        print(f"[Pix] Gerando QR Code para R${valor:.2f}...")
        return StatusPagamento.PENDENTE