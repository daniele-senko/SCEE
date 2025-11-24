"""Serviço de autenticação.

Fornece operações de registro de clientes e autenticação de usuários.

Este módulo define um protocolo para repositório de usuários e a classe
`AuthService` com métodos:

- ``registrar_cliente(nome, email, senha, cpf) -> Cliente``
- ``login(email, senha) -> Usuario``

Exemplo de uso::

    from src.services.auth_service import AuthService, UsuarioRepository
    from src.infra.usuario_repo_memory import UsuarioRepoMemory  # exemplo

    repo: UsuarioRepository = UsuarioRepoMemory()
    auth = AuthService(repo)

    cliente = auth.registrar_cliente("João", "j@ex.com", "senha123", "12345678901")
    usuario = auth.login("j@ex.com", "senha123")

As funções de hash/cheque de senha são usadas a partir de ``src.utils.security``
({{gerar_hash_senha, verificar_senha}}) — o módulo é assumido existente no projeto.
"""

from __future__ import annotations

from typing import Protocol, Optional

from src.models.users.client_model import Cliente
from src.models.users.user_model import Usuario
from src.utils.security import gerar_hash_senha, verificar_senha


class UsuarioRepository(Protocol):
    """Protocolo que descreve a interface mínima esperada de um repositório de usuários.

    Implementações concretas devem prover busca por e-mail e salvamento de entidades.
    """

    def buscar_por_email(self, email: str) -> Optional[Usuario]:
        ...

    def salvar(self, usuario: Usuario) -> Usuario:
        ...


class AuthService:
    """Serviço de autenticação responsável por registrar clientes e efetuar login.

    Regras principais:
    - ``registrar_cliente`` valida dados, cria hash de senha, verifica duplicidade
      de e-mail e persiste o cliente via repositório.
    - ``login`` valida credenciais usando o repositório e a função ``verificar_senha``.

    Em caso de dados inválidos ou credenciais incorretas, um ``ValueError`` é levantado.
    """

    def __init__(self, usuario_repository: UsuarioRepository) -> None:
        self._repo = usuario_repository

    def registrar_cliente(self, nome: str, email: str, senha: str, cpf: str) -> Cliente:
        """Registra um novo cliente.

        Valida os dados do cliente, assegura que o e-mail não esteja em uso,
        gera o hash da senha e persiste o cliente.

        :param nome: Nome completo do cliente
        :param email: E-mail único para login
        :param senha: Senha em texto plano (será hasheada)
        :param cpf: CPF do cliente (será validado pelo modelo)
        :return: Cliente persistido
        :raises ValueError: se dados inválidos ou e-mail já cadastrado
        """
        # Verifica se já existe usuário com o e-mail
        existente = self._repo.buscar_por_email(email)
        if existente is not None:
            raise ValueError("E-mail já cadastrado.")

        # Gera hash de senha
        senha_hash = gerar_hash_senha(senha)

        # Cria instância de Cliente e valida (raise ValueError em caso de falha)
        cliente = Cliente(nome=nome, email=email, cpf=cpf, senha_hash=senha_hash)
        cliente.validar()

        # Persiste e retorna o objeto salvo
        salvo = self._repo.salvar(cliente)
        return salvo

    def login(self, email: str, senha: str) -> Usuario:
        """Autentica um usuário pelo e-mail e senha.

        :param email: E-mail do usuário
        :param senha: Senha em texto plano
        :return: Instância de ``Usuario`` autenticada
        :raises ValueError: se credenciais inválidas
        """
        usuario = self._repo.buscar_por_email(email)
        if usuario is None:
            raise ValueError("Credenciais inválidas.")

        senha_hash = usuario.senha_hash
        if not verificar_senha(senha, senha_hash):
            raise ValueError("Credenciais inválidas.")

        return usuario

