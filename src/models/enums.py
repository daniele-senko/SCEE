from enum import Enum
# O módulo 'enum' é nativo do Python e facilita a criação de constantes fixas.

# --- ENUMERAÇÕES PARA CLASSES DE ENTIDADES (MODELS) ---

class TipoUsuario(str, Enum):
    """
    Define os tipos de usuários que podem acessar o sistema.
    
    A herança de (str, Enum) garante que o valor armazenado no banco de dados 
    seja a string literal ('cliente', 'admin'), facilitando a leitura e consulta SQL.
    
    Uso: models/administrador.py, models/cliente.py, services/auth_service.py
    """
    CLIENTE = 'cliente'
    ADMIN = 'admin'

class StatusPedido(str, Enum):
    """
    Define os possíveis estágios no ciclo de vida de um Pedido (EPIC 5).
    
    O 'CheckoutService' (SCEE-57) utilizará 'PROCESSANDO' ou 'PAGAMENTO_PENDENTE' 
    como status inicial após a finalização da compra.
    """
    PROCESSANDO = 'PROCESSANDO'         # Pagamento aprovado, aguardando separação/envio.
    ENVIADO = 'ENVIADO'                 # Pedido despachado, código de rastreio anexado.
    ENTREGUE = 'ENTREGUE'               # Cliente confirmou o recebimento.
    CANCELADO = 'CANCELADO'             # Pedido cancelado (ex: falha de estoque ou cliente).
    PAGAMENTO_PENDENTE = 'PAGAMENTO_PENDENTE' # Pagamento falhou ou está em análise (ex: PIX não pago).

# --- ENUMERAÇÕES PARA INTEGRAÇÃO E SERVIÇOS ---

class StatusPagamento(str, Enum):
    """
    Define os status que são RETORNADOS pela API/Interface de Pagamento.
    
    Esta é a resposta padrão que o 'CheckoutService' (SCEE-57) espera para tomar a decisão 
    de criar ou não o Pedido e abater o estoque.
    """
    APROVADO = 'APROVADO'   # Pagamento confirmado.
    REJEITADO = 'REJEITADO' # Pagamento negado (cartão inválido, limite, etc.).
    PENDENTE = 'PENDENTE'   # Pagamento em análise ou aguardando ação (ex: PIX, boleto).

class TipoFrete(str, Enum):
    """
    Define os tipos de métodos de entrega disponíveis.
    
    Usado pelo CheckoutService para determinar o método de envio.
    """
    CORREIOS_PAC = 'PAC'
    CORREIOS_SEDEX = 'SEDEX'
    RETIRADA_LOCAL = 'RETIRADA_LOCAL'