class PriceValidator:
    """
    Validador especializado para valores monetários e numéricos positivos.
    Garante integridade financeira básica.
    """

    @staticmethod
    def validate_price(value: float) -> bool:
        """
        Verifica se o preço é um número positivo.
        :param value: Valor float
        :return: True se válido
        """
        if not isinstance(value, (int, float)):
            return False
        return value >= 0.0

    @staticmethod
    def validate_stock(value: int) -> bool:
        """
        Verifica se o estoque é um inteiro não-negativo.
        :param value: Quantidade
        :return: True se válido
        """
        if not isinstance(value, int):
            return False
        return value >= 0