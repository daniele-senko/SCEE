import re

class CpfValidator:
    """
    Responsável exclusivamente pela validação de CPF.
    """

    @staticmethod
    def validate(cpf: str) -> bool:
        """
        Verifica se o CPF possui 11 dígitos numéricos.
        :param cpf: string do CPF (com ou sem pontuação)
        :return: True se válido, False se inválido
        """
        if not cpf:
            return False
            
        # Remove tudo que não for número
        cpf_limpo = re.sub(r'\D', '', cpf)
        
        # Verifica se tem 11 dígitos
        return len(cpf_limpo) == 11