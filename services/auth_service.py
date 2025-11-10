"""Placeholder: AuthService (esqueleto).

Este arquivo é um stub/touch — implementar lógica real posteriormente.
"""

class AuthService:
    def __init__(self, usuario_repository):
        self.usuario_repository = usuario_repository

    def register(self, data):
        # implementar: validação, hash de senha, persistência
        raise NotImplementedError

    def login(self, email, senha):
        # implementar: verificar credenciais e gerar token
        raise NotImplementedError
