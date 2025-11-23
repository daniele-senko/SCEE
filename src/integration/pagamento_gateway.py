import abc
from typing import Dict, Any
# Importamos o Enum de status para tipagem e retorno padrão
from src.models.enums import StatusPagamento 

# --- INTERFACE ABSTRATA (PILAR DO POLIMORFISMO) ---

class GatewayPagamentoBase(abc.ABC):
    """
    Classe Abstrata (Interface) para todos os Gateways de Pagamento.
    
    O DEV 2 deve injetar uma instância desta interface no CheckoutService.
    Esta classe garante que, seja qual for o método de pagamento, ele terá 
    o método 'processar_pagamento' (CONTRATO).
    """

    @abc.abstractmethod
    def processar_pagamento(self, valor: float, dados_pagamento: Dict[str, Any]) -> StatusPagamento:
        """
        Método abstrato que deve ser OBRIGATORIAMENTE implementado por cada classe filha.
        
        Args:
            valor: O valor total do pedido a ser cobrado.
            dados_pagamento: Informações específicas do método (cartão, pix, etc.).
        
        Returns:
            StatusPagamento: APROVADO, REJEITADO ou PENDENTE.
        """
        pass

# --- IMPLEMENTAÇÃO CONCRETA (SIMULAÇÃO) ---

class PagamentoCartao(GatewayPagamentoBase):
    """
    Implementação Concreta de um Gateway de Cartão de Crédito.
    
    Esta classe cumpre o contrato de 'GatewayPagamentoBase'.
    Ela simula a chamada a uma API de terceiros (ex: Cielo, Pagar.me).
    """
    
    def processar_pagamento(self, valor: float, dados_cartao: Dict[str, Any]) -> StatusPagamento:
        """
        Simula a comunicação e a resposta de um Gateway de Cartão.
        """
        
        # [LÓGICA DE NEGÓCIO DA SIMULAÇÃO]
        # 1. Validação Mínima
        if valor <= 0 or 'numero' not in dados_cartao:
            print("[PagamentoCartao] Transação REJEITADA: Dados inválidos.")
            return StatusPagamento.REJEITADO
        
        # 2. Simulação de Risco/Limite
        if valor > 1500.00:
            # Simula a rejeição de um valor alto (para testar o ROLLBACK no CheckoutService)
            print(f"[PagamentoCartao] Transação de R${valor:.2f} REJEITADA por Alto Risco (Simulação).")
            return StatusPagamento.REJEITADO
            
        # 3. Simulação de Aprovação
        print(f"[PagamentoCartao] Transação de R${valor:.2f} APROVADA.")
        return StatusPagamento.APROVADO

class PagamentoPix(GatewayPagamentoBase):
    """
    Implementação Concreta para processamento via PIX.
    
    O PIX é assíncrono. Esta classe simula a geração do QR Code.
    """
    def processar_pagamento(self, valor: float, dados_pix: Dict[str, Any]) -> StatusPagamento:
        # Em um sistema real, aqui você chamaria a API bancária para gerar o QR Code.
        print(f"[PagamentoPix] Gerando QR Code PIX para R${valor:.2f}. Status PENDENTE.")
        # Retorna PENDENTE, o que fará o CheckoutService criar o Pedido com StatusPedido.PAGAMENTO_PENDENTE.
        return StatusPagamento.PENDENTE