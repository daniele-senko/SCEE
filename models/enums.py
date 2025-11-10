"""Placeholder: Enums do domínio (StatusPedido, TipoPagamento)."""

from enum import Enum


class StatusPedido(str, Enum):
    PENDENTE = "PENDENTE"
    PROCESSANDO = "PROCESSANDO"
    ENVIADO = "ENVIADO"
    ENTREGUE = "ENTREGUE"


class TipoPagamento(str, Enum):
    CARTAO = "CARTAO"
    PIX = "PIX"
