"""Serviço de gerenciamento de usuários.

Implementa lógica de negócio para gerenciamento de perfil, senhas,
permissões e validações de usuários.
"""
from typing import List, Dict, Any, Optional
import re
from passlib.hash import bcrypt
from repositories.usuario_repository import UsuarioRepository
from repositories.endereco_repository import EnderecoRepository


class UsuarioServiceError(Exception):
    """Exceção base para erros do UsuarioService."""
    pass


class UsuarioNaoEncontradoError(UsuarioServiceError):
    """Usuário não foi encontrado."""
    pass


class EmailInvalidoError(UsuarioServiceError):
    """Email é inválido."""
    pass


class SenhaFracaError(UsuarioServiceError):
    """Senha não atende aos requisitos de segurança."""
    pass


class PermissaoNegadaError(UsuarioServiceError):
    """Usuário não tem permissão para a operação."""
    pass


class UsuarioService:
    """Serviço para gerenciamento de usuários."""
    
    # Tipos de usuário
    TIPO_CLIENTE = 'cliente'
    TIPO_ADMINISTRADOR = 'administrador'
    TIPOS_VALIDOS = {TIPO_CLIENTE, TIPO_ADMINISTRADOR}
    
    # Validação de senha
    MIN_SENHA_LENGTH = 8
    MAX_SENHA_LENGTH = 128
    
    # Validação de nome
    MIN_NOME_LENGTH = 3
    MAX_NOME_LENGTH = 200
    
    # Pattern de email
    EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    
    def __init__(
        self,
        usuario_repo: UsuarioRepository,
        endereco_repo: Optional[EnderecoRepository] = None
    ):
        """Inicializa o serviço com os repositórios necessários.
        
        Args:
            usuario_repo: Repositório de usuários
            endereco_repo: Repositório de endereços (opcional)
        """
        self.usuario_repo = usuario_repo
        self.endereco_repo = endereco_repo
    
    def buscar_por_id(
        self,
        usuario_id: int,
        incluir_enderecos: bool = False
    ) -> Dict[str, Any]:
        """Busca um usuário por ID.
        
        Args:
            usuario_id: ID do usuário
            incluir_enderecos: Se True, inclui endereços do usuário
            
        Returns:
            Dados do usuário
            
        Raises:
            UsuarioNaoEncontradoError: Usuário não encontrado
        """
        usuario = self.usuario_repo.buscar_por_id(usuario_id)
        if not usuario:
            raise UsuarioNaoEncontradoError(f"Usuário {usuario_id} não encontrado")
        
        # Remover senha_hash dos dados retornados
        usuario_seguro = self._remover_dados_sensiveis(usuario)
        
        # Incluir endereços se solicitado
        if incluir_enderecos and self.endereco_repo:
            enderecos = self.endereco_repo.listar_por_usuario(usuario_id)
            usuario_seguro['enderecos'] = enderecos
        
        return usuario_seguro
    
    def buscar_por_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Busca um usuário por email.
        
        Args:
            email: Email do usuário
            
        Returns:
            Dados do usuário ou None
        """
        usuario = self.usuario_repo.buscar_por_email(email)
        if not usuario:
            return None
        
        return self._remover_dados_sensiveis(usuario)
    
    def atualizar_perfil(
        self,
        usuario_id: int,
        nome: Optional[str] = None,
        email: Optional[str] = None,
        usuario_solicitante_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Atualiza o perfil de um usuário.
        
        Args:
            usuario_id: ID do usuário a atualizar
            nome: Novo nome (opcional)
            email: Novo email (opcional)
            usuario_solicitante_id: ID do usuário fazendo a requisição
            
        Returns:
            Usuário atualizado
            
        Raises:
            UsuarioNaoEncontradoError: Usuário não encontrado
            PermissaoNegadaError: Sem permissão para atualizar
            EmailInvalidoError: Email inválido ou já em uso
        """
        # Buscar usuário
        usuario = self.usuario_repo.buscar_por_id(usuario_id)
        if not usuario:
            raise UsuarioNaoEncontradoError(f"Usuário {usuario_id} não encontrado")
        
        # Validar permissões (só pode atualizar próprio perfil ou ser admin)
        if usuario_solicitante_id:
            self._validar_permissao_edicao(usuario_id, usuario_solicitante_id)
        
        # Atualizar nome
        if nome is not None:
            self._validar_nome(nome)
            usuario['nome'] = nome
        
        # Atualizar email
        if email is not None:
            self._validar_email(email)
            
            # Verificar se email já está em uso
            usuario_existente = self.usuario_repo.buscar_por_email(email)
            if usuario_existente and usuario_existente['id'] != usuario_id:
                raise EmailInvalidoError("Email já está em uso")
            
            usuario['email'] = email
        
        # Atualizar no banco
        self.usuario_repo.atualizar(usuario)
        
        return self._remover_dados_sensiveis(usuario)
    
    def alterar_senha(
        self,
        usuario_id: int,
        senha_atual: str,
        nova_senha: str
    ) -> bool:
        """Altera a senha de um usuário.
        
        Args:
            usuario_id: ID do usuário
            senha_atual: Senha atual
            nova_senha: Nova senha
            
        Returns:
            True se senha alterada com sucesso
            
        Raises:
            UsuarioNaoEncontradoError: Usuário não encontrado
            UsuarioServiceError: Senha atual incorreta
            SenhaFracaError: Nova senha não atende requisitos
        """
        # Buscar usuário
        usuario = self.usuario_repo.buscar_por_id(usuario_id)
        if not usuario:
            raise UsuarioNaoEncontradoError(f"Usuário {usuario_id} não encontrado")
        
        # Verificar senha atual
        if not bcrypt.verify(senha_atual, usuario['senha_hash']):
            raise UsuarioServiceError("Senha atual incorreta")
        
        # Validar nova senha
        self._validar_senha(nova_senha)
        
        # Verificar se nova senha é diferente da atual
        if bcrypt.verify(nova_senha, usuario['senha_hash']):
            raise UsuarioServiceError("Nova senha deve ser diferente da atual")
        
        # Atualizar senha
        usuario['senha_hash'] = bcrypt.hash(nova_senha)
        self.usuario_repo.atualizar(usuario)
        
        return True
    
    def resetar_senha(
        self,
        usuario_id: int,
        nova_senha: str,
        usuario_admin_id: int
    ) -> bool:
        """Reseta a senha de um usuário (apenas admin).
        
        Args:
            usuario_id: ID do usuário
            nova_senha: Nova senha
            usuario_admin_id: ID do administrador fazendo a operação
            
        Returns:
            True se senha resetada com sucesso
            
        Raises:
            PermissaoNegadaError: Usuário não é admin
            UsuarioNaoEncontradoError: Usuário não encontrado
            SenhaFracaError: Senha não atende requisitos
        """
        # Validar que usuário solicitante é admin
        self._validar_admin(usuario_admin_id)
        
        # Buscar usuário
        usuario = self.usuario_repo.buscar_por_id(usuario_id)
        if not usuario:
            raise UsuarioNaoEncontradoError(f"Usuário {usuario_id} não encontrado")
        
        # Validar nova senha
        self._validar_senha(nova_senha)
        
        # Atualizar senha
        usuario['senha_hash'] = bcrypt.hash(nova_senha)
        self.usuario_repo.atualizar(usuario)
        
        return True
    
    def promover_a_admin(
        self,
        usuario_id: int,
        usuario_admin_id: int
    ) -> Dict[str, Any]:
        """Promove um usuário a administrador.
        
        Args:
            usuario_id: ID do usuário a promover
            usuario_admin_id: ID do administrador fazendo a operação
            
        Returns:
            Usuário atualizado
            
        Raises:
            PermissaoNegadaError: Usuário não é admin
            UsuarioNaoEncontradoError: Usuário não encontrado
        """
        # Validar que usuário solicitante é admin
        self._validar_admin(usuario_admin_id)
        
        # Buscar usuário
        usuario = self.usuario_repo.buscar_por_id(usuario_id)
        if not usuario:
            raise UsuarioNaoEncontradoError(f"Usuário {usuario_id} não encontrado")
        
        # Atualizar tipo
        usuario['tipo'] = self.TIPO_ADMINISTRADOR
        self.usuario_repo.atualizar(usuario)
        
        return self._remover_dados_sensiveis(usuario)
    
    def rebaixar_de_admin(
        self,
        usuario_id: int,
        usuario_admin_id: int
    ) -> Dict[str, Any]:
        """Rebaixa um administrador a cliente.
        
        Args:
            usuario_id: ID do usuário a rebaixar
            usuario_admin_id: ID do administrador fazendo a operação
            
        Returns:
            Usuário atualizado
            
        Raises:
            PermissaoNegadaError: Sem permissão ou tentando rebaixar a si mesmo
            UsuarioNaoEncontradoError: Usuário não encontrado
        """
        # Validar que usuário solicitante é admin
        self._validar_admin(usuario_admin_id)
        
        # Não pode rebaixar a si mesmo
        if usuario_id == usuario_admin_id:
            raise PermissaoNegadaError("Não é possível rebaixar a si mesmo")
        
        # Buscar usuário
        usuario = self.usuario_repo.buscar_por_id(usuario_id)
        if not usuario:
            raise UsuarioNaoEncontradoError(f"Usuário {usuario_id} não encontrado")
        
        # Atualizar tipo
        usuario['tipo'] = self.TIPO_CLIENTE
        self.usuario_repo.atualizar(usuario)
        
        return self._remover_dados_sensiveis(usuario)
    
    def listar_usuarios(
        self,
        tipo: Optional[str] = None,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """Lista usuários com filtros opcionais.
        
        Args:
            tipo: Filtrar por tipo (cliente/administrador)
            limit: Limite de resultados
            offset: Offset para paginação
            
        Returns:
            Lista de usuários
        """
        usuarios = self.usuario_repo.listar(limit, offset)
        
        # Filtrar por tipo se especificado
        if tipo:
            usuarios = [u for u in usuarios if u.get('tipo') == tipo]
        
        # Remover dados sensíveis
        return [self._remover_dados_sensiveis(u) for u in usuarios]
    
    def obter_estatisticas(self) -> Dict[str, Any]:
        """Obtém estatísticas de usuários.
        
        Returns:
            Dicionário com estatísticas
        """
        total_clientes = self.usuario_repo.contar_por_tipo(self.TIPO_CLIENTE)
        total_admins = self.usuario_repo.contar_por_tipo(self.TIPO_ADMINISTRADOR)
        
        return {
            'total_usuarios': total_clientes + total_admins,
            'total_clientes': total_clientes,
            'total_administradores': total_admins
        }
    
    def validar_credenciais(self, email: str, senha: str) -> Optional[Dict[str, Any]]:
        """Valida credenciais de login.
        
        Args:
            email: Email do usuário
            senha: Senha do usuário
            
        Returns:
            Dados do usuário se credenciais válidas, None caso contrário
        """
        usuario = self.usuario_repo.buscar_por_email(email)
        if not usuario:
            return None
        
        # Verificar senha
        if not bcrypt.verify(senha, usuario['senha_hash']):
            return None
        
        return self._remover_dados_sensiveis(usuario)
    
    def eh_admin(self, usuario_id: int) -> bool:
        """Verifica se um usuário é administrador.
        
        Args:
            usuario_id: ID do usuário
            
        Returns:
            True se é administrador
        """
        try:
            usuario = self.usuario_repo.buscar_por_id(usuario_id)
            return usuario and usuario.get('tipo') == self.TIPO_ADMINISTRADOR
        except:
            return False
    
    # Métodos privados de validação
    
    def _validar_nome(self, nome: str) -> None:
        """Valida o nome do usuário."""
        if not nome or not nome.strip():
            raise UsuarioServiceError("Nome não pode ser vazio")
        
        if len(nome) < self.MIN_NOME_LENGTH:
            raise UsuarioServiceError(
                f"Nome deve ter pelo menos {self.MIN_NOME_LENGTH} caracteres"
            )
        
        if len(nome) > self.MAX_NOME_LENGTH:
            raise UsuarioServiceError(
                f"Nome não pode ter mais de {self.MAX_NOME_LENGTH} caracteres"
            )
    
    def _validar_email(self, email: str) -> None:
        """Valida o formato do email."""
        if not email or not email.strip():
            raise EmailInvalidoError("Email não pode ser vazio")
        
        if not self.EMAIL_PATTERN.match(email):
            raise EmailInvalidoError("Formato de email inválido")
    
    def _validar_senha(self, senha: str) -> None:
        """Valida a força da senha."""
        if not senha:
            raise SenhaFracaError("Senha não pode ser vazia")
        
        if len(senha) < self.MIN_SENHA_LENGTH:
            raise SenhaFracaError(
                f"Senha deve ter pelo menos {self.MIN_SENHA_LENGTH} caracteres"
            )
        
        if len(senha) > self.MAX_SENHA_LENGTH:
            raise SenhaFracaError(
                f"Senha não pode ter mais de {self.MAX_SENHA_LENGTH} caracteres"
            )
        
        # Verificar complexidade
        tem_letra = any(c.isalpha() for c in senha)
        tem_numero = any(c.isdigit() for c in senha)
        
        if not (tem_letra and tem_numero):
            raise SenhaFracaError(
                "Senha deve conter pelo menos uma letra e um número"
            )
    
    def _validar_admin(self, usuario_id: int) -> None:
        """Valida se o usuário é administrador."""
        usuario = self.usuario_repo.buscar_por_id(usuario_id)
        if not usuario or usuario.get('tipo') != self.TIPO_ADMINISTRADOR:
            raise PermissaoNegadaError("Operação requer permissões de administrador")
    
    def _validar_permissao_edicao(
        self,
        usuario_id: int,
        usuario_solicitante_id: int
    ) -> None:
        """Valida se o usuário tem permissão para editar."""
        # Pode editar próprio perfil
        if usuario_id == usuario_solicitante_id:
            return
        
        # Ou ser admin
        if not self.eh_admin(usuario_solicitante_id):
            raise PermissaoNegadaError(
                "Você não tem permissão para editar este perfil"
            )
    
    def _remover_dados_sensiveis(self, usuario: Dict[str, Any]) -> Dict[str, Any]:
        """Remove dados sensíveis do usuário."""
        usuario_seguro = dict(usuario)
        usuario_seguro.pop('senha_hash', None)
        return usuario_seguro
