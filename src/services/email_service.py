"""Serviço de envio de emails.

Implementa lógica de negócio para envio de emails com templates,
validações, retry logic e filas (simuladas).
"""
from typing import List, Dict, Any, Optional
import re
import logging
from datetime import datetime
from decimal import Decimal
from enum import Enum


# Configurar logger
logger = logging.getLogger(__name__)


class TipoEmail(Enum):
    """Tipos de email suportados."""
    BEM_VINDO = 'bem_vindo'
    CONFIRMACAO_PEDIDO = 'confirmacao_pedido'
    ATUALIZACAO_PEDIDO = 'atualizacao_pedido'
    PEDIDO_ENVIADO = 'pedido_enviado'
    PEDIDO_ENTREGUE = 'pedido_entregue'
    PEDIDO_CANCELADO = 'pedido_cancelado'
    RESETAR_SENHA = 'resetar_senha'
    NOTIFICACAO_GERAL = 'notificacao_geral'


class EmailServiceError(Exception):
    """Exceção base para erros do EmailService."""
    pass


class EmailInvalidoError(EmailServiceError):
    """Email é inválido."""
    pass


class TemplateNaoEncontradoError(EmailServiceError):
    """Template de email não encontrado."""
    pass


class EnvioEmailError(EmailServiceError):
    """Erro ao enviar email."""
    pass


class EmailService:
    """Serviço para envio de emails com templates e retry logic."""
    
    # Pattern de validação de email
    EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    
    # Configurações de retry
    MAX_TENTATIVAS = 3
    TIMEOUT_SEGUNDOS = 30
    
    # Limite de emails por lote
    MAX_EMAILS_POR_LOTE = 50
    
    def __init__(
        self,
        smtp_host: Optional[str] = None,
        smtp_port: Optional[int] = None,
        smtp_user: Optional[str] = None,
        smtp_password: Optional[str] = None,
        remetente: str = "noreply@scee.com.br",
        modo_mock: bool = True
    ):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.remetente = remetente
        self.modo_mock = modo_mock
        
        self.fila_emails: List[Dict[str, Any]] = []
        self.historico: List[Dict[str, Any]] = []
    
    def enviar_email(
        self,
        destinatario: str,
        assunto: str,
        corpo: str,
        copias: Optional[List[str]] = None,
        prioridade: int = 5
    ) -> bool:
        """Envia um email simples."""
        self._validar_email(destinatario)
        
        if copias:
            for email in copias:
                self._validar_email(email)
        
        if not assunto or not assunto.strip():
            raise EmailServiceError("Assunto não pode ser vazio")
        
        if not corpo or not corpo.strip():
            raise EmailServiceError("Corpo do email não pode ser vazio")
        
        email_data = {
            'id': self._gerar_id_email(),
            'destinatario': destinatario,
            'assunto': assunto,
            'corpo': corpo,
            'copias': copias or [],
            'prioridade': prioridade,
            'tentativas': 0,
            'criado_em': datetime.now(),
            'enviado': False
        }
        
        return self._enviar_com_retry(email_data)
    
    def enviar_email_template(
        self,
        destinatario: str,
        tipo: TipoEmail,
        dados: Dict[str, Any]
    ) -> bool:
        """Envia um email usando template."""
        assunto, corpo = self._gerar_email_template(tipo, dados)
        return self.enviar_email(destinatario, assunto, corpo)
    
    def enviar_bem_vindo(self, usuario: Dict[str, Any]) -> bool:
        return self.enviar_email_template(
            destinatario=usuario['email'],
            tipo=TipoEmail.BEM_VINDO,
            dados={'nome': usuario['nome']}
        )
    
    def enviar_confirmacao_pedido(
        self,
        usuario: Dict[str, Any],
        pedido: Dict[str, Any]
    ) -> bool:
        """Envia email de confirmação de pedido."""
        # CORREÇÃO AQUI: Tenta pegar 'valor_total' (novo padrão) ou 'total' (legado)
        valor_total = pedido.get('valor_total', pedido.get('total', 0.0))
        
        return self.enviar_email_template(
            destinatario=usuario['email'],
            tipo=TipoEmail.CONFIRMACAO_PEDIDO,
            dados={
                'nome': usuario['nome'],
                'pedido_id': pedido['id'],
                'total': valor_total, # Passa para o template como 'total'
                'itens': pedido.get('itens', [])
            }
        )
    
    def enviar_atualizacao_pedido(
        self,
        usuario: Dict[str, Any],
        pedido: Dict[str, Any],
        novo_status: str
    ) -> bool:
        """Envia email de atualização de status do pedido."""
        if novo_status == 'ENVIADO':
            tipo = TipoEmail.PEDIDO_ENVIADO
        elif novo_status == 'ENTREGUE':
            tipo = TipoEmail.PEDIDO_ENTREGUE
        elif novo_status == 'CANCELADO':
            tipo = TipoEmail.PEDIDO_CANCELADO
        else:
            tipo = TipoEmail.ATUALIZACAO_PEDIDO
        
        return self.enviar_email_template(
            destinatario=usuario['email'],
            tipo=tipo,
            dados={
                'nome': usuario['nome'],
                'pedido_id': pedido['id'],
                'status': novo_status
            }
        )
    
    def enviar_resetar_senha(
        self,
        usuario: Dict[str, Any],
        token: str
    ) -> bool:
        return self.enviar_email_template(
            destinatario=usuario['email'],
            tipo=TipoEmail.RESETAR_SENHA,
            dados={
                'nome': usuario['nome'],
                'token': token,
                'link': f"https://scee.com.br/reset-senha?token={token}"
            }
        )
    
    # ... (Mantenha o restante dos métodos de lote, fila e histórico iguais) ...

    def enviar_lote(self, destinatarios: List[str], assunto: str, corpo: str) -> Dict[str, Any]:
        if len(destinatarios) > self.MAX_EMAILS_POR_LOTE:
            raise EmailServiceError(f"Máximo de {self.MAX_EMAILS_POR_LOTE} emails por lote")
        
        sucessos = 0
        falhas = 0
        erros = []
        
        for destinatario in destinatarios:
            try:
                if self.enviar_email(destinatario, assunto, corpo):
                    sucessos += 1
                else:
                    falhas += 1
            except Exception as e:
                falhas += 1
                erros.append({'destinatario': destinatario, 'erro': str(e)})
        
        return {'total': len(destinatarios), 'sucessos': sucessos, 'falhas': falhas, 'erros': erros}
    
    def adicionar_a_fila(self, destinatario: str, assunto: str, corpo: str, prioridade: int = 5) -> str:
        email_id = self._gerar_id_email()
        self.fila_emails.append({
            'id': email_id, 'destinatario': destinatario, 'assunto': assunto,
            'corpo': corpo, 'prioridade': prioridade, 'tentativas': 0,
            'criado_em': datetime.now(), 'enviado': False
        })
        self.fila_emails.sort(key=lambda x: x['prioridade'])
        logger.info(f"Email {email_id} adicionado à fila")
        return email_id
    
    def processar_fila(self, limite: Optional[int] = None) -> Dict[str, Any]:
        processados = 0
        sucessos = 0
        falhas = 0
        emails_a_processar = self.fila_emails[:limite] if limite else self.fila_emails
        
        for email_data in emails_a_processar:
            processados += 1
            if self._enviar_com_retry(email_data):
                sucessos += 1
                self.fila_emails.remove(email_data)
            else:
                falhas += 1
                if email_data['tentativas'] >= self.MAX_TENTATIVAS:
                    self.fila_emails.remove(email_data)
        
        return {'processados': processados, 'sucessos': sucessos, 'falhas': falhas, 'restantes_na_fila': len(self.fila_emails)}
    
    def obter_historico(self, limite: Optional[int] = None) -> List[Dict[str, Any]]:
        historico = sorted(self.historico, key=lambda x: x.get('enviado_em', datetime.min), reverse=True)
        if limite: return historico[:limite]
        return historico
    
    # Métodos privados
    
    def _validar_email(self, email: str) -> None:
        if not email or not email.strip():
            raise EmailInvalidoError("Email não pode ser vazio")
        if not self.EMAIL_PATTERN.match(email):
            raise EmailInvalidoError(f"Formato de email inválido: {email}")
    
    def _gerar_id_email(self) -> str:
        return f"email_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
    
    def _enviar_com_retry(self, email_data: Dict[str, Any]) -> bool:
        while email_data['tentativas'] < self.MAX_TENTATIVAS:
            email_data['tentativas'] += 1
            try:
                if self._enviar_real(email_data):
                    email_data['enviado'] = True
                    email_data['enviado_em'] = datetime.now()
                    self.historico.append(dict(email_data))
                    logger.info(f"Email enviado com sucesso para {email_data['destinatario']}")
                    return True
            except Exception as e:
                logger.warning(f"Falha ao enviar email (tentativa {email_data['tentativas']}): {str(e)}")
        logger.error(f"Falha definitiva ao enviar email após {self.MAX_TENTATIVAS} tentativas")
        return False
    
    def _enviar_real(self, email_data: Dict[str, Any]) -> bool:
        if self.modo_mock:
            print(f"\n[EMAIL MOCK] Enviando para: {email_data['destinatario']}")
            print(f"Assunto: {email_data['assunto']}")
            print("-" * 30)
            return True
        else:
            raise NotImplementedError("Envio real de email não implementado ainda")
    
    def _gerar_email_template(self, tipo: TipoEmail, dados: Dict[str, Any]) -> tuple[str, str]:
        templates = {
            TipoEmail.BEM_VINDO: (
                "Bem-vindo ao SCEE!",
                f"Olá {dados.get('nome', 'Cliente')},\n\nSeja bem-vindo ao SCEE!\nAtenciosamente,\nEquipe SCEE"
            ),
            TipoEmail.CONFIRMACAO_PEDIDO: (
                f"Pedido #{dados.get('pedido_id')} confirmado!",
                f"Olá {dados.get('nome', 'Cliente')},\n\nSeu pedido #{dados.get('pedido_id')} foi confirmado!\n"
                f"Valor total: R$ {dados.get('total', 0):.2f}\n\nAtenciosamente,\nEquipe SCEE"
            ),
            TipoEmail.PEDIDO_ENVIADO: (
                f"Pedido #{dados.get('pedido_id')} enviado!",
                f"Olá {dados.get('nome', 'Cliente')},\n\nSeu pedido #{dados.get('pedido_id')} foi enviado!\nAtenciosamente,\nEquipe SCEE"
            ),
            TipoEmail.PEDIDO_ENTREGUE: (
                f"Pedido #{dados.get('pedido_id')} entregue!",
                f"Olá {dados.get('nome', 'Cliente')},\n\nSeu pedido #{dados.get('pedido_id')} foi entregue!\nAtenciosamente,\nEquipe SCEE"
            ),
            TipoEmail.PEDIDO_CANCELADO: (
                f"Pedido #{dados.get('pedido_id')} cancelado",
                f"Olá {dados.get('nome', 'Cliente')},\n\nSeu pedido #{dados.get('pedido_id')} foi cancelado.\nAtenciosamente,\nEquipe SCEE"
            ),
            TipoEmail.RESETAR_SENHA: (
                "Redefinição de senha - SCEE",
                f"Olá {dados.get('nome', 'Cliente')},\n\nClique no link: {dados.get('link', '#')}\nAtenciosamente,\nEquipe SCEE"
            ),
            TipoEmail.ATUALIZACAO_PEDIDO: (
                f"Atualização do pedido #{dados.get('pedido_id')}",
                f"Olá {dados.get('nome', 'Cliente')},\n\nNovo status: {dados.get('status', 'N/A')}\nAtenciosamente,\nEquipe SCEE"
            )
        }
        
        if tipo not in templates:
            raise TemplateNaoEncontradoError(f"Template {tipo.value} não encontrado")
        
        return templates[tipo]