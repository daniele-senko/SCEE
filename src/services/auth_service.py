"""
AuthService - Serviço de Autenticação
Gerencia login, registro e validação de usuários
"""

import logging
from typing import Optional, Dict
from passlib.hash import bcrypt

logger = logging.getLogger(__name__)


class AuthService:
    """Serviço de autenticação de usuários"""
    
    def __init__(self, usuario_repository):
        """
        Inicializa o serviço de autenticação
        
        Args:
            usuario_repository: Repositório de usuários
        """
        self.usuario_repository = usuario_repository

    def register(self, data: Dict) -> Optional[Dict]:
        """
        Registra um novo usuário
        
        Args:
            data: Dados do usuário (nome, email, senha, etc.)
            
        Returns:
            Dados do usuário criado ou None se falhar
        """
        try:
            # Validar dados
            if not data.get('email') or not data.get('senha'):
                logger.error("Email e senha são obrigatórios")
                return None
                
            # Verificar se email já existe
            existing_user = self.usuario_repository.buscar_por_email(data['email'])
            if existing_user:
                logger.error(f"Email já cadastrado: {data['email']}")
                return None
            
            # Hash da senha
            hashed_password = bcrypt.hash(data['senha'])
            
            # Criar dados do usuário
            user_data = {
                'nome': data.get('nome', ''),
                'email': data['email'],
                'senha_hash': hashed_password,
                'tipo_usuario': data.get('tipo_usuario', 'CLIENTE'),
                'ativo': True
            }
            
            # Criar usuário
            user_id = self.usuario_repository.criar(user_data)
            
            if user_id:
                logger.info(f"Usuário registrado com sucesso: {data['email']}")
                return self.usuario_repository.buscar_por_id(user_id)
            
            return None
            
        except Exception as e:
            logger.error(f"Erro ao registrar usuário: {e}", exc_info=True)
            return None

    def login(self, email: str, senha: str) -> Optional[Dict]:
        """
        Realiza login do usuário
        
        Args:
            email: Email do usuário
            senha: Senha do usuário
            
        Returns:
            Dados do usuário se credenciais válidas, None caso contrário
        """
        try:
            # Buscar usuário por email
            user = self.usuario_repository.buscar_por_email(email)
            
            if not user:
                logger.warning(f"Usuário não encontrado: {email}")
                return None
            
            # Verificar se usuário está ativo
            if not user.get('ativo', False):
                logger.warning(f"Usuário inativo: {email}")
                return None
            
            # Verificar senha
            if not bcrypt.verify(senha, user.get('senha_hash', '')):
                logger.warning(f"Senha incorreta para: {email}")
                return None
            
            logger.info(f"Login bem-sucedido: {email}")
            
            # Remover senha do retorno
            user_data = {k: v for k, v in user.items() if k != 'senha_hash'}
            
            return user_data
            
        except Exception as e:
            logger.error(f"Erro ao fazer login: {e}", exc_info=True)
            return None
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verifica se a senha está correta
        
        Args:
            plain_password: Senha em texto plano
            hashed_password: Senha hasheada
            
        Returns:
            True se a senha está correta, False caso contrário
        """
        try:
            return bcrypt.verify(plain_password, hashed_password)
        except Exception as e:
            logger.error(f"Erro ao verificar senha: {e}")
            return False
    
    def hash_password(self, password: str) -> str:
        """
        Gera hash de uma senha
        
        Args:
            password: Senha em texto plano
            
        Returns:
            Hash da senha
        """
        return bcrypt.hash(password)
    
    def change_password(self, user_id: int, old_password: str, new_password: str) -> bool:
        """
        Altera a senha do usuário
        
        Args:
            user_id: ID do usuário
            old_password: Senha antiga
            new_password: Senha nova
            
        Returns:
            True se senha foi alterada, False caso contrário
        """
        try:
            # Buscar usuário
            user = self.usuario_repository.buscar_por_id(user_id)
            
            if not user:
                logger.error(f"Usuário não encontrado: {user_id}")
                return False
            
            # Verificar senha antiga
            if not bcrypt.verify(old_password, user.get('senha_hash', '')):
                logger.warning(f"Senha antiga incorreta para usuário: {user_id}")
                return False
            
            # Hash da nova senha
            new_hash = bcrypt.hash(new_password)
            
            # Atualizar senha
            success = self.usuario_repository.atualizar(user_id, {'senha_hash': new_hash})
            
            if success:
                logger.info(f"Senha alterada com sucesso para usuário: {user_id}")
            
            return success
            
        except Exception as e:
            logger.error(f"Erro ao alterar senha: {e}", exc_info=True)
            return False

