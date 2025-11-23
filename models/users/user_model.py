from utils.validators.email_validator import EmailValidator

class Usuario:
    """
    Classe Base que representa um usuário genérico do sistema.
    Deve ser herdada por Cliente e Administrador.
    """

    def __init__(self, nome: str, email: str, senha_hash: str, id: int = None):
        """
        Construtor da classe Usuario.
        :param nome: Nome completo
        :param email: E-mail para login
        :param senha_hash: Senha já criptografada
        :param id: ID do banco de dados (opcional na criação)
        """
        self._id = id
        self.nome = nome
        self._email = None # Atributo protegido
        self.senha_hash = senha_hash
        
        # Setter do email faz a validação
        self.email = email 

    @property
    def id(self):
        """Getter para o ID (somente leitura para evitar alteração acidental)."""
        return self._id

    @property
    def email(self):
        """Getter para o e-mail."""
        return self._email

    @email.setter
    def email(self, valor: str):
        """
        Setter para o e-mail com validação.
        Lança erro se o formato for inválido.
        """
        if not EmailValidator.validate(valor):
            raise ValueError(f"E-mail inválido: {valor}")
        self._email = valor

    def __str__(self):
        return f"{self.nome} ({self.email})"