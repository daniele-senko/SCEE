from models.users.user_model import Usuario

class Administrador(Usuario):
    """
    Representa um usuário administrativo com permissões de gestão.
    """

    def __init__(self, nome: str, email: str, senha_hash: str, nivel_acesso: str = "padrao", id: int = None):
        super().__init__(nome, email, senha_hash, id)
        self.nivel_acesso = nivel_acesso # ex: 'gerente', 'estoquista'

    def tem_permissao_gerencial(self) -> bool:
        """Verifica se o admin é um gerente."""
        return self.nivel_acesso.lower() == "gerente"

    def __repr__(self):
        return f"<Admin: {self.nome} - Nível: {self.nivel_acesso}>"