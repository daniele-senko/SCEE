from typing import Dict, Any
from src.models.enums import StatusPagamento
from .payment_gateway import PaymentGateway

class CreditCardGateway(PaymentGateway):
    def processar_pagamento(self, valor: float, dados: Dict[str, Any]) -> StatusPagamento:
        print(f"[Cartão] Processando R${valor:.2f}...")
        
        # Validação simples
        if valor <= 0:
            return StatusPagamento.REJEITADO
            
        # Simulação de aprovação
        return StatusPagamento.APROVADO