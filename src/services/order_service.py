"""Serviço de gerenciamento de pedidos.

Implementa lógica de negócio para operações de pedidos com validações
de status, transições, cancelamento e consultas avançadas.
"""
from typing import List, Dict, Any, Optional, Set
from decimal import Decimal
from datetime import datetime, timedelta
from src.repositories.order_repository import PedidoRepository
from src.repositories.product_repository import ProductRepository
from src.repositories.user_repository import UsuarioRepository


class PedidoServiceError(Exception):
    """Exceção base para erros do PedidoService."""
    pass


class StatusInvalidoError(PedidoServiceError):
    """Status do pedido é inválido."""
    pass


class TransicaoStatusInvalidaError(PedidoServiceError):
    """Transição de status não é permitida."""
    pass


class PedidoNaoEncontradoError(PedidoServiceError):
    """Pedido não foi encontrado."""
    pass


class CancelamentoNaoPermitidoError(PedidoServiceError):
    """Cancelamento do pedido não é permitido."""
    pass


class PedidoService:
    """Serviço para gerenciamento de pedidos."""
    
    # Status válidos
    STATUS_PENDENTE = 'PENDENTE'
    STATUS_PROCESSANDO = 'PROCESSANDO'
    STATUS_ENVIADO = 'ENVIADO'
    STATUS_ENTREGUE = 'ENTREGUE'
    STATUS_CANCELADO = 'CANCELADO'
    
    TODOS_STATUS = {
        STATUS_PENDENTE,
        STATUS_PROCESSANDO,
        STATUS_ENVIADO,
        STATUS_ENTREGUE,
        STATUS_CANCELADO
    }
    
    # Transições válidas de status
    TRANSICOES_VALIDAS = {
        STATUS_PENDENTE: {STATUS_PROCESSANDO, STATUS_CANCELADO},
        STATUS_PROCESSANDO: {STATUS_ENVIADO, STATUS_CANCELADO},
        STATUS_ENVIADO: {STATUS_ENTREGUE},
        STATUS_ENTREGUE: set(),  # Estado final
        STATUS_CANCELADO: set()  # Estado final
    }
    
    # Tempo limite para cancelamento (em horas)
    TEMPO_LIMITE_CANCELAMENTO = 24
    
    def __init__(
        self,
        pedido_repo: PedidoRepository,
        produto_repo: ProductRepository,
        usuario_repo: UsuarioRepository
    ):
        """Inicializa o serviço com os repositórios necessários.
        
        Args:
            pedido_repo: Repositório de pedidos
            produto_repo: Repositório de produtos
            usuario_repo: Repositório de usuários
        """
        self.pedido_repo = pedido_repo
        self.produto_repo = produto_repo
        self.usuario_repo = usuario_repo
    
    def criar_pedido(
        self,
        usuario_id: int,
        endereco_id: int,
        itens: List[Dict[str, Any]],
        tipo_pagamento: str,
        frete: float = 0.0,
        observacoes: Optional[str] = None
    ) -> Dict[str, Any]:
        """Cria um novo pedido.
        
        Args:
            usuario_id: ID do usuário
            endereco_id: ID do endereço de entrega
            itens: Lista de itens [{produto_id, quantidade, preco_unitario}]
            tipo_pagamento: Tipo de pagamento (CARTAO, BOLETO, PIX)
            frete: Valor do frete
            observacoes: Observações do pedido
            
        Returns:
            Pedido criado
            
        Raises:
            PedidoServiceError: Validações básicas
        """
        # Validações básicas
        if not itens:
            raise PedidoServiceError("Pedido deve conter pelo menos um item")
        
        if usuario_id <= 0:
            raise PedidoServiceError("ID de usuário inválido")
        
        if endereco_id <= 0:
            raise PedidoServiceError("ID de endereço inválido")
        
        # Validar tipo de pagamento
        tipos_validos = {'CARTAO', 'BOLETO', 'PIX'}
        if tipo_pagamento not in tipos_validos:
            raise PedidoServiceError(
                f"Tipo de pagamento inválido. Valores válidos: {tipos_validos}"
            )
        
        # Calcular subtotal
        subtotal = Decimal('0.00')
        for item in itens:
            if item['quantidade'] <= 0:
                raise PedidoServiceError("Quantidade deve ser maior que zero")
            if item['preco_unitario'] <= 0:
                raise PedidoServiceError("Preço unitário deve ser maior que zero")
            
            subtotal += Decimal(str(item['quantidade'])) * Decimal(str(item['preco_unitario']))
        
        # Calcular total
        frete_decimal = Decimal(str(frete))
        total = subtotal + frete_decimal
        
        # Criar pedido
        try:
            pedido = self.pedido_repo.salvar({
                'usuario_id': usuario_id,
                'endereco_id': endereco_id,
                'subtotal': float(subtotal),
                'frete': float(frete_decimal),
                'total': float(total),
                'status': self.STATUS_PENDENTE,
                'tipo_pagamento': tipo_pagamento,
                'observacoes': observacoes
            })
            
            # Adicionar itens
            for item in itens:
                # Buscar nome do produto
                produto = self.produto_repo.buscar_por_id(item['produto_id'])
                if not produto:
                    raise PedidoServiceError(f"Produto {item['produto_id']} não encontrado")
                
                self.pedido_repo.adicionar_item(
                    pedido['id'],
                    item['produto_id'],
                    produto['nome'],
                    item['quantidade'],
                    item['preco_unitario']
                )
            
            return pedido
            
        except Exception as e:
            raise PedidoServiceError(f"Erro ao criar pedido: {str(e)}")
    
    def buscar_por_id(self, pedido_id: int, completo: bool = False) -> Optional[Dict[str, Any]]:
        """Busca um pedido por ID.
        
        Args:
            pedido_id: ID do pedido
            completo: Se True, busca com todos os detalhes (itens, endereço)
            
        Returns:
            Dados do pedido ou None
        """
        if completo:
            return self.pedido_repo.buscar_completo(pedido_id)
        return self.pedido_repo.buscar_por_id(pedido_id)
    
    def listar_pedidos_usuario(
        self,
        usuario_id: int,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """Lista pedidos de um usuário.
        
        Args:
            usuario_id: ID do usuário
            limit: Número máximo de pedidos
            offset: Offset para paginação
            
        Returns:
            Lista de pedidos
        """
        return self.pedido_repo.listar_por_usuario(usuario_id, limit, offset)
    
    def listar_pedidos_por_status(
        self,
        status: str,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """Lista pedidos por status.
        
        Args:
            status: Status do pedido
            limit: Número máximo de pedidos
            offset: Offset para paginação
            
        Returns:
            Lista de pedidos
            
        Raises:
            StatusInvalidoError: Status inválido
        """
        self._validar_status(status)
        return self.pedido_repo.listar_por_status(status, limit, offset)
    
    def atualizar_status(
        self,
        pedido_id: int,
        novo_status: str,
        validar_transicao: bool = True
    ) -> bool:
        """Atualiza o status de um pedido.
        
        Args:
            pedido_id: ID do pedido
            novo_status: Novo status
            validar_transicao: Se True, valida se a transição é permitida
            
        Returns:
            True se atualizado com sucesso
            
        Raises:
            PedidoNaoEncontradoError: Pedido não encontrado
            StatusInvalidoError: Status inválido
            TransicaoStatusInvalidaError: Transição não permitida
        """
        # Validar status
        self._validar_status(novo_status)
        
        # Buscar pedido
        pedido = self.pedido_repo.buscar_por_id(pedido_id)
        if not pedido:
            raise PedidoNaoEncontradoError(f"Pedido {pedido_id} não encontrado")
        
        # Validar transição
        if validar_transicao:
            self._validar_transicao_status(pedido['status'], novo_status)
        
        return self.pedido_repo.atualizar_status(pedido_id, novo_status)
    
    def cancelar_pedido(
        self,
        pedido_id: int,
        usuario_id: Optional[int] = None,
        motivo: Optional[str] = None
    ) -> bool:
        """Cancela um pedido e ESTORNA o estoque."""
        
        # Buscar pedido COMPLETO (com itens) para saber o que devolver
        pedido = self.pedido_repo.buscar_completo(pedido_id) # Certifique-se que seu repo tem esse método ou similar
        if not pedido:
            raise PedidoNaoEncontradoError(f"Pedido {pedido_id} não encontrado")
        
        # Validar propriedade (se for cliente)
        if usuario_id and pedido['usuario_id'] != usuario_id:
            raise CancelamentoNaoPermitidoError("Pedido pertence a outro usuário")
        
        # Validar se cancelamento é permitido (Regra de Status e Tempo)
        if not self._pode_cancelar(pedido):
            raise CancelamentoNaoPermitidoError(
                f"Pedido no status '{pedido['status']}' não pode ser cancelado"
            )
        
        # ESTORNO DE ESTOQUE
        try:
            # Iteramos sobre os itens do pedido para devolver a quantidade
            for item in pedido.get('itens', []):
                produto = self.produto_repo.buscar_por_id(item['produto_id'])
                if produto:
                    # Se o repo retornar dict:
                    novo_estoque = int(produto['estoque']) + int(item['quantidade'])
                    # Atualiza apenas o campo estoque (ou o produto todo se o repo exigir)
                    produto['estoque'] = novo_estoque
                    self.produto_repo.atualizar(produto)
                    
                    # Se o repo retornar Objeto, seria:
                    # produto.estoque += item['quantidade']
                    # self.produto_repo.atualizar(produto)

        except Exception as e:
            # Logar erro crítico aqui (estoque pode ficar inconsistente se falhar no meio)
            print(f"Erro crítico ao estornar estoque: {e}")
            raise e

        # Atualizar status do pedido
        observacoes = pedido.get('observacoes', '') or ''
        if motivo:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            observacoes += f"\n[CANCELADO em {timestamp}] {motivo}"
        
        # Precisamos passar apenas os dados atualizáveis para o repo, ou o objeto todo
        pedido['status'] = self.STATUS_CANCELADO
        pedido['observacoes'] = observacoes
        
        self.pedido_repo.atualizar_status(pedido['id'], self.STATUS_CANCELADO) 
        # Ou self.pedido_repo.atualizar(pedido) se atualizar tudo

        return True
    
    def obter_estatisticas(self, usuario_id: Optional[int] = None) -> Dict[str, Any]:
        """Obtém estatísticas de pedidos.
        
        Args:
            usuario_id: Opcional, filtrar por usuário
            
        Returns:
            Dicionário com estatísticas
        """
        estatisticas = {
            'total_pedidos': 0,
            'por_status': {},
            'total_vendas': 0.0
        }
        
        # Contar por status
        for status in self.TODOS_STATUS:
            count = self.pedido_repo.contar_por_status(status)
            estatisticas['por_status'][status] = count
            estatisticas['total_pedidos'] += count
        
        # Calcular total de vendas
        estatisticas['total_vendas'] = self.pedido_repo.calcular_total_vendas(usuario_id)
        
        return estatisticas
    
    def pode_avaliar(self, pedido_id: int, usuario_id: int) -> bool:
        """Verifica se o usuário pode avaliar o pedido.
        
        Args:
            pedido_id: ID do pedido
            usuario_id: ID do usuário
            
        Returns:
            True se pode avaliar
        """
        pedido = self.pedido_repo.buscar_por_id(pedido_id)
        if not pedido:
            return False
        
        # Só pode avaliar se for o dono do pedido e estiver entregue
        return (
            pedido['usuario_id'] == usuario_id and
            pedido['status'] == self.STATUS_ENTREGUE
        )
    
    def obter_historico_completo(self, pedido_id: int) -> Dict[str, Any]:
        """Obtém histórico completo do pedido com todos os detalhes.
        
        Args:
            pedido_id: ID do pedido
            
        Returns:
            Dicionário com pedido completo e metadados
            
        Raises:
            PedidoNaoEncontradoError: Pedido não encontrado
        """
        pedido_completo = self.pedido_repo.buscar_completo(pedido_id)
        if not pedido_completo:
            raise PedidoNaoEncontradoError(f"Pedido {pedido_id} não encontrado")
        
        # Adicionar metadados
        pedido_completo['pode_cancelar'] = self._pode_cancelar(pedido_completo)
        pedido_completo['status_final'] = pedido_completo['status'] in {
            self.STATUS_ENTREGUE, self.STATUS_CANCELADO
        }
        pedido_completo['proximos_status'] = list(
            self.TRANSICOES_VALIDAS.get(pedido_completo['status'], set())
        )
        
        return pedido_completo
    
    # Métodos privados de validação
    
    def _validar_status(self, status: str) -> None:
        """Valida se o status é válido."""
        if status not in self.TODOS_STATUS:
            raise StatusInvalidoError(
                f"Status '{status}' inválido. Valores válidos: {self.TODOS_STATUS}"
            )
    
    def _validar_transicao_status(self, status_atual: str, novo_status: str) -> None:
        """Valida se a transição de status é permitida."""
        if novo_status not in self.TRANSICOES_VALIDAS.get(status_atual, set()):
            raise TransicaoStatusInvalidaError(
                f"Transição de '{status_atual}' para '{novo_status}' não é permitida"
            )
    
    def _pode_cancelar(self, pedido: Dict[str, Any]) -> bool:
        """Verifica se o pedido pode ser cancelado.
        
        Args:
            pedido: Dados do pedido
            
        Returns:
            True se pode ser cancelado
        """
        # Só pode cancelar pedidos PENDENTE ou PROCESSANDO
        if pedido['status'] not in {self.STATUS_PENDENTE, self.STATUS_PROCESSANDO}:
            return False
        
        # Verificar tempo limite
        if 'criado_em' in pedido:
            criado_em = pedido['criado_em']
            if isinstance(criado_em, str):
                criado_em = datetime.strptime(criado_em, '%Y-%m-%d %H:%M:%S')
            
            tempo_decorrido = datetime.now() - criado_em
            if tempo_decorrido > timedelta(hours=self.TEMPO_LIMITE_CANCELAMENTO):
                return False
        
        return True
