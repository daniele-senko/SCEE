import re

class EmailValidator:
    """
    Responsável exclusivamente pela validação de formatos de e-mail.
    """

    @staticmethod
    def validate(email: str) -> bool:
        """
        Verifica se o e-mail corresponde ao padrão regex.
        :param email: string do e-mail
        :return: True se válido, False se inválido
        """
        if not email:
            return False
            
        # Padrão Regex comum para e-mails
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None