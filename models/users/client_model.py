from models.users.user_model import Usuario
from utils.validators.cpf_validator import CpfValidator

class Cliente(Usuario):
    """
    Representa o cliente da loja.
    Herda atributos e métodos da classe Usuario.
    """

    def __init__(self, nome: str, email: str, cpf: str, senha_hash: str, id: int = None):
        # Chama o construtor da classe pai (Usuario) para configurar nome, email, senha
        super().__init__(nome, email, senha_hash, id)
        
        self._cpf = None
        self.cpf = cpf # Usa o setter para validar

    @property
    def cpf(self):
        return self._cpf

    @cpf.setter
    def cpf(self, valor: str):
        if not CpfValidator.validate(valor):
            raise ValueError(f"CPF inválido: {valor}")
        self._cpf = valor

    def __repr__(self):
        return f"<Cliente: {self.nome} - CPF: {self.cpf}>"