from enum import Enum

# --- ENUMERAÇÕES PARA CLASSES DE ENTIDADES (MODELS) ---

class TipoUsuario(str, Enum):
    CLIENTE = 'cliente'
    ADMIN = 'admin'

class StatusPedido(str, Enum):
    """
    Define os estágios do Pedido.
    IMPORTANTE: O valor (str) deve bater com a Check Constraint do Banco de Dados.
    """
    PROCESSANDO = 'PROCESSANDO'
    ENVIADO = 'ENVIADO'
    ENTREGUE = 'ENTREGUE'
    CANCELADO = 'CANCELADO'
    # CORREÇÃO: Mudamos de 'PAGAMENTO_PENDENTE' para 'PENDENTE'
    # Isso alinha o código Python com a regra CHECK(status IN ('PENDENTE'...)) do SQLite
    PAGAMENTO_PENDENTE = 'PENDENTE' 

# --- ENUMERAÇÕES PARA INTEGRAÇÃO E SERVIÇOS ---

class StatusPagamento(str, Enum):
    APROVADO = 'APROVADO'
    REJEITADO = 'REJEITADO'
    PENDENTE = 'PENDENTE'

class TipoFrete(str, Enum):
    CORREIOS_PAC = 'PAC'
    CORREIOS_SEDEX = 'SEDEX'
    RETIRADA_LOCAL = 'RETIRADA_LOCAL'