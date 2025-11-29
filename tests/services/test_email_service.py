"""Testes para o EmailService."""
import pytest
from src.services.email_service import (
    EmailService,
    TipoEmail,
    EmailServiceError,
    EmailInvalidoError
)


class TestEmailService:
    """Testes do serviço de email."""
    
    def test_enviar_email_sucesso(self):
        """Testa envio de email simples."""
        service = EmailService(modo_mock=True)
        
        resultado = service.enviar_email(
            destinatario='teste@email.com',
            assunto='Assunto Teste',
            corpo='Corpo do email de teste'
        )
        
        assert resultado is True
        assert len(service.historico) == 1
    
    def test_enviar_email_invalido(self):
        """Testa erro com email inválido."""
        service = EmailService(modo_mock=True)
        
        with pytest.raises(EmailInvalidoError):
            service.enviar_email(
                destinatario='email-invalido',
                assunto='Teste',
                corpo='Teste'
            )
    
    def test_enviar_email_assunto_vazio(self):
        """Testa erro com assunto vazio."""
        service = EmailService(modo_mock=True)
        
        with pytest.raises(EmailServiceError, match="Assunto não pode ser vazio"):
            service.enviar_email(
                destinatario='teste@email.com',
                assunto='',
                corpo='Corpo do email'
            )
    
    def test_enviar_bem_vindo(self):
        """Testa envio de email de boas-vindas."""
        service = EmailService(modo_mock=True)
        
        usuario = {
            'email': 'novo@email.com',
            'nome': 'Novo Usuário'
        }
        
        resultado = service.enviar_bem_vindo(usuario)
        
        assert resultado is True
        assert len(service.historico) == 1
        assert 'Bem-vindo' in service.historico[0]['assunto']
    
    def test_enviar_confirmacao_pedido(self):
        """Testa envio de confirmação de pedido."""
        service = EmailService(modo_mock=True)
        
        usuario = {'email': 'cliente@email.com', 'nome': 'Cliente Teste'}
        pedido = {'id': 123, 'total': 299.90, 'itens': []}
        
        resultado = service.enviar_confirmacao_pedido(usuario, pedido)
        
        assert resultado is True
        assert 'Pedido #123' in service.historico[0]['assunto']
    
    def test_enviar_atualizacao_pedido_enviado(self):
        """Testa envio de atualização de pedido enviado."""
        service = EmailService(modo_mock=True)
        
        usuario = {'email': 'cliente@email.com', 'nome': 'Cliente'}
        pedido = {'id': 456}
        
        resultado = service.enviar_atualizacao_pedido(usuario, pedido, 'ENVIADO')
        
        assert resultado is True
        assert 'enviado' in service.historico[0]['assunto'].lower()
    
    def test_enviar_resetar_senha(self):
        """Testa envio de email para resetar senha."""
        service = EmailService(modo_mock=True)
        
        usuario = {'email': 'usuario@email.com', 'nome': 'Usuário'}
        token = 'abc123xyz'
        
        resultado = service.enviar_resetar_senha(usuario, token)
        
        assert resultado is True
        assert 'senha' in service.historico[0]['assunto'].lower()
        assert token in service.historico[0]['corpo']
    
    def test_enviar_lote(self):
        """Testa envio de emails em lote."""
        service = EmailService(modo_mock=True)
        
        destinatarios = [
            'user1@email.com',
            'user2@email.com',
            'user3@email.com'
        ]
        
        resultado = service.enviar_lote(
            destinatarios=destinatarios,
            assunto='Newsletter',
            corpo='Conteúdo da newsletter'
        )
        
        assert resultado['total'] == 3
        assert resultado['sucessos'] == 3
        assert resultado['falhas'] == 0
    
    def test_adicionar_a_fila(self):
        """Testa adição de email à fila."""
        service = EmailService(modo_mock=True)
        
        email_id = service.adicionar_a_fila(
            destinatario='teste@email.com',
            assunto='Teste',
            corpo='Corpo do teste',
            prioridade=1
        )
        
        assert email_id is not None
        assert len(service.fila_emails) == 1
    
    def test_processar_fila(self):
        """Testa processamento da fila de emails."""
        service = EmailService(modo_mock=True)
        
        # Adicionar emails à fila
        service.adicionar_a_fila('email1@test.com', 'Assunto 1', 'Corpo 1')
        service.adicionar_a_fila('email2@test.com', 'Assunto 2', 'Corpo 2')
        
        # Processar fila
        resultado = service.processar_fila()
        
        assert resultado['processados'] >= 1  # Pelo menos 1 processado
        assert resultado['sucessos'] >= 1
        assert resultado['restantes_na_fila'] >= 0
    
    def test_obter_historico(self):
        """Testa obtenção do histórico de emails."""
        service = EmailService(modo_mock=True)
        
        # Enviar alguns emails
        service.enviar_email('teste1@email.com', 'Assunto 1', 'Corpo 1')
        service.enviar_email('teste2@email.com', 'Assunto 2', 'Corpo 2')
        
        # Obter histórico
        historico = service.obter_historico()
        
        assert len(historico) == 2
        assert all('enviado_em' in email for email in historico)
    
    def test_obter_historico_com_limite(self):
        """Testa obtenção do histórico com limite."""
        service = EmailService(modo_mock=True)
        
        # Enviar vários emails
        for i in range(5):
            service.enviar_email(f'teste{i}@email.com', f'Assunto {i}', f'Corpo {i}')
        
        # Obter apenas 3 mais recentes
        historico = service.obter_historico(limite=3)
        
        assert len(historico) == 3
