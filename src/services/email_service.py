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
        """Inicializa o serviço de email.
        
        Args:
            smtp_host: Host do servidor SMTP
            smtp_port: Porta do servidor SMTP
            smtp_user: Usuário SMTP
            smtp_password: Senha SMTP
            remetente: Email remetente padrão
            modo_mock: Se True, simula envio sem enviar emails reais
        """
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.remetente = remetente
        self.modo_mock = modo_mock
        
        # Fila de emails (em memória)
        self.fila_emails: List[Dict[str, Any]] = []
        
        # Histórico de envios
        self.historico: List[Dict[str, Any]] = []
    
    def enviar_email(
        self,
        destinatario: str,
        assunto: str,
        corpo: str,
        copias: Optional[List[str]] = None,
        prioridade: int = 5
    ) -> bool:
        """Envia um email simples.
        
        Args:
            destinatario: Email do destinatário
            assunto: Assunto do email
            corpo: Corpo do email (texto ou HTML)
            copias: Lista de emails em cópia (opcional)
            prioridade: Prioridade (1-10, sendo 1 mais alta)
            
        Returns:
            True se enviado com sucesso
            
        Raises:
            EmailInvalidoError: Email inválido
            EnvioEmailError: Erro ao enviar
        """
        # Validar destinatário
        self._validar_email(destinatario)
        
        # Validar cópias
        if copias:
            for email in copias:
                self._validar_email(email)
        
        # Validar assunto e corpo
        if not assunto or not assunto.strip():
            raise EmailServiceError("Assunto não pode ser vazio")
        
        if not corpo or not corpo.strip():
            raise EmailServiceError("Corpo do email não pode ser vazio")
        
        # Criar dados do email
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
        
        # Tentar enviar
        return self._enviar_com_retry(email_data)
    
    def enviar_email_template(
        self,
        destinatario: str,
        tipo: TipoEmail,
        dados: Dict[str, Any]
    ) -> bool:
        """Envia um email usando template.
        
        Args:
            destinatario: Email do destinatário
            tipo: Tipo do email (template)
            dados: Dados para preencher o template
            
        Returns:
            True se enviado com sucesso
            
        Raises:
            EmailInvalidoError: Email inválido
            TemplateNaoEncontradoError: Template não encontrado
        """
        # Gerar email a partir do template
        assunto, corpo = self._gerar_email_template(tipo, dados)
        
        # Enviar email
        return self.enviar_email(destinatario, assunto, corpo)
    
    def enviar_bem_vindo(self, usuario: Dict[str, Any]) -> bool:
        """Envia email de boas-vindas a novo usuário.
        
        Args:
            usuario: Dados do usuário
            
        Returns:
            True se enviado com sucesso
        """
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
        """Envia email de confirmação de pedido.
        
        Args:
            usuario: Dados do usuário
            pedido: Dados do pedido
            
        Returns:
            True se enviado com sucesso
        """
        return self.enviar_email_template(
            destinatario=usuario['email'],
            tipo=TipoEmail.CONFIRMACAO_PEDIDO,
            dados={
                'nome': usuario['nome'],
                'pedido_id': pedido['id'],
                'total': pedido['total'],
                'itens': pedido.get('itens', [])
            }
        )
    
    def enviar_atualizacao_pedido(
        self,
        usuario: Dict[str, Any],
        pedido: Dict[str, Any],
        novo_status: str
    ) -> bool:
        """Envia email de atualização de status do pedido.
        
        Args:
            usuario: Dados do usuário
            pedido: Dados do pedido
            novo_status: Novo status do pedido
            
        Returns:
            True se enviado com sucesso
        """
        # Determinar tipo de email baseado no status
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
        """Envia email para resetar senha.
        
        Args:
            usuario: Dados do usuário
            token: Token de reset de senha
            
        Returns:
            True se enviado com sucesso
        """
        return self.enviar_email_template(
            destinatario=usuario['email'],
            tipo=TipoEmail.RESETAR_SENHA,
            dados={
                'nome': usuario['nome'],
                'token': token,
                'link': f"https://scee.com.br/reset-senha?token={token}"
            }
        )
    
    def enviar_lote(
        self,
        destinatarios: List[str],
        assunto: str,
        corpo: str
    ) -> Dict[str, Any]:
        """Envia email para múltiplos destinatários.
        
        Args:
            destinatarios: Lista de emails
            assunto: Assunto do email
            corpo: Corpo do email
            
        Returns:
            Dicionário com resultado do envio
        """
        if len(destinatarios) > self.MAX_EMAILS_POR_LOTE:
            raise EmailServiceError(
                f"Máximo de {self.MAX_EMAILS_POR_LOTE} emails por lote"
            )
        
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
                erros.append({
                    'destinatario': destinatario,
                    'erro': str(e)
                })
        
        return {
            'total': len(destinatarios),
            'sucessos': sucessos,
            'falhas': falhas,
            'erros': erros
        }
    
    def adicionar_a_fila(
        self,
        destinatario: str,
        assunto: str,
        corpo: str,
        prioridade: int = 5
    ) -> str:
        """Adiciona email à fila para envio posterior.
        
        Args:
            destinatario: Email do destinatário
            assunto: Assunto
            corpo: Corpo do email
            prioridade: Prioridade (1-10)
            
        Returns:
            ID do email na fila
        """
        email_id = self._gerar_id_email()
        
        self.fila_emails.append({
            'id': email_id,
            'destinatario': destinatario,
            'assunto': assunto,
            'corpo': corpo,
            'prioridade': prioridade,
            'tentativas': 0,
            'criado_em': datetime.now(),
            'enviado': False
        })
        
        # Ordenar fila por prioridade
        self.fila_emails.sort(key=lambda x: x['prioridade'])
        
        logger.info(f"Email {email_id} adicionado à fila")
        return email_id
    
    def processar_fila(self, limite: Optional[int] = None) -> Dict[str, Any]:
        """Processa emails na fila.
        
        Args:
            limite: Número máximo de emails a processar
            
        Returns:
            Estatísticas do processamento
        """
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
                # Se excedeu tentativas, remover da fila
                if email_data['tentativas'] >= self.MAX_TENTATIVAS:
                    self.fila_emails.remove(email_data)
        
        return {
            'processados': processados,
            'sucessos': sucessos,
            'falhas': falhas,
            'restantes_na_fila': len(self.fila_emails)
        }
    
    def obter_historico(
        self,
        limite: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Obtém histórico de emails enviados.
        
        Args:
            limite: Número máximo de registros
            
        Returns:
            Lista de emails enviados
        """
        historico = sorted(
            self.historico,
            key=lambda x: x.get('enviado_em', datetime.min),
            reverse=True
        )
        
        if limite:
            return historico[:limite]
        return historico
    
    # Métodos privados
    
    def _validar_email(self, email: str) -> None:
        """Valida formato de email."""
        if not email or not email.strip():
            raise EmailInvalidoError("Email não pode ser vazio")
        
        if not self.EMAIL_PATTERN.match(email):
            raise EmailInvalidoError(f"Formato de email inválido: {email}")
    
    def _gerar_id_email(self) -> str:
        """Gera ID único para email."""
        return f"email_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
    
    def _enviar_com_retry(self, email_data: Dict[str, Any]) -> bool:
        """Envia email com retry logic.
        
        Args:
            email_data: Dados do email
            
        Returns:
            True se enviado com sucesso
        """
        while email_data['tentativas'] < self.MAX_TENTATIVAS:
            email_data['tentativas'] += 1
            
            try:
                # Simular envio
                if self._enviar_real(email_data):
                    email_data['enviado'] = True
                    email_data['enviado_em'] = datetime.now()
                    
                    # Adicionar ao histórico
                    self.historico.append(dict(email_data))
                    
                    logger.info(
                        f"Email enviado com sucesso para {email_data['destinatario']} "
                        f"(tentativa {email_data['tentativas']})"
                    )
                    return True
                
            except Exception as e:
                logger.warning(
                    f"Falha ao enviar email para {email_data['destinatario']} "
                    f"(tentativa {email_data['tentativas']}): {str(e)}"
                )
        
        logger.error(
            f"Falha definitiva ao enviar email para {email_data['destinatario']} "
            f"após {self.MAX_TENTATIVAS} tentativas"
        )
        return False
    
    def _enviar_real(self, email_data: Dict[str, Any]) -> bool:
        """Envia email real ou simula envio.
        
        Args:
            email_data: Dados do email
            
        Returns:
            True se enviado com sucesso
        """
        if self.modo_mock:
            # Modo mock - apenas loga
            logger.info(
                f"[MOCK] Enviando email:\n"
                f"  De: {self.remetente}\n"
                f"  Para: {email_data['destinatario']}\n"
                f"  Assunto: {email_data['assunto']}\n"
                f"  Corpo: {email_data['corpo'][:100]}..."
            )
            return True
        else:
            # Modo real - implementar SMTP aqui
            # import smtplib
            # from email.mime.text import MIMEText
            # ...
            raise NotImplementedError("Envio real de email não implementado ainda")
    
    def _gerar_email_template(
        self,
        tipo: TipoEmail,
        dados: Dict[str, Any]
    ) -> tuple[str, str]:
        """Gera assunto e corpo do email a partir de template.
        
        Args:
            tipo: Tipo do email
            dados: Dados para preencher o template
            
        Returns:
            Tupla (assunto, corpo)
        """
        templates = {
            TipoEmail.BEM_VINDO: (
                "Bem-vindo ao SCEE!",
                f"Olá {dados.get('nome', 'Cliente')},\n\n"
                f"Seja bem-vindo ao SCEE - Sistema de Comércio Eletrônico!\n\n"
                f"Estamos felizes em tê-lo conosco.\n\n"
                f"Atenciosamente,\nEquipe SCEE"
            ),
            TipoEmail.CONFIRMACAO_PEDIDO: (
                f"Pedido #{dados.get('pedido_id')} confirmado!",
                f"Olá {dados.get('nome', 'Cliente')},\n\n"
                f"Seu pedido #{dados.get('pedido_id')} foi confirmado com sucesso!\n\n"
                f"Valor total: R$ {dados.get('total', 0):.2f}\n\n"
                f"Você receberá atualizações sobre o status do seu pedido.\n\n"
                f"Atenciosamente,\nEquipe SCEE"
            ),
            TipoEmail.PEDIDO_ENVIADO: (
                f"Pedido #{dados.get('pedido_id')} enviado!",
                f"Olá {dados.get('nome', 'Cliente')},\n\n"
                f"Seu pedido #{dados.get('pedido_id')} foi enviado!\n\n"
                f"Em breve você receberá seus produtos.\n\n"
                f"Atenciosamente,\nEquipe SCEE"
            ),
            TipoEmail.PEDIDO_ENTREGUE: (
                f"Pedido #{dados.get('pedido_id')} entregue!",
                f"Olá {dados.get('nome', 'Cliente')},\n\n"
                f"Seu pedido #{dados.get('pedido_id')} foi entregue!\n\n"
                f"Esperamos que esteja satisfeito com sua compra.\n\n"
                f"Atenciosamente,\nEquipe SCEE"
            ),
            TipoEmail.PEDIDO_CANCELADO: (
                f"Pedido #{dados.get('pedido_id')} cancelado",
                f"Olá {dados.get('nome', 'Cliente')},\n\n"
                f"Seu pedido #{dados.get('pedido_id')} foi cancelado.\n\n"
                f"Se você não solicitou o cancelamento, entre em contato conosco.\n\n"
                f"Atenciosamente,\nEquipe SCEE"
            ),
            TipoEmail.RESETAR_SENHA: (
                "Redefinição de senha - SCEE",
                f"Olá {dados.get('nome', 'Cliente')},\n\n"
                f"Você solicitou a redefinição de senha.\n\n"
                f"Clique no link abaixo para redefinir:\n"
                f"{dados.get('link', '#')}\n\n"
                f"Este link expira em 24 horas.\n\n"
                f"Se você não solicitou, ignore este email.\n\n"
                f"Atenciosamente,\nEquipe SCEE"
            ),
            TipoEmail.ATUALIZACAO_PEDIDO: (
                f"Atualização do pedido #{dados.get('pedido_id')}",
                f"Olá {dados.get('nome', 'Cliente')},\n\n"
                f"Seu pedido #{dados.get('pedido_id')} foi atualizado.\n\n"
                f"Novo status: {dados.get('status', 'N/A')}\n\n"
                f"Atenciosamente,\nEquipe SCEE"
            )
        }
        
        if tipo not in templates:
            raise TemplateNaoEncontradoError(f"Template {tipo.value} não encontrado")
        
        return templates[tipo]
