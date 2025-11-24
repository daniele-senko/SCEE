from datetime import datetime

class Formatter:
    """
    Classe utilitária para formatação visual de dados na interface (UI).
    Responsável por converter dados brutos (int, float, date) para o padrão brasileiro.
    """

    @staticmethod
    def format_currency(value: float) -> str:
        """
        Formata um número float para o padrão monetário brasileiro (R$).
        Ex: 1200.50 -> 'R$ 1.200,50'
        """
        if value is None:
            return "R$ 0,00"
            
        # Formata com 2 casas decimais e vírgula de milhar no padrão US primeiro
        # Ex: 1,234.56
        texto = f"{value:,.2f}"
        
        # Inverte os caracteres: vírgula vira ponto, ponto vira vírgula
        # Truque: Troca , por v (temporário), . por , e v por .
        texto = texto.replace(',', 'v').replace('.', ',').replace('v', '.')
        
        return f"R$ {texto}"

    @staticmethod
    def format_date(date_obj: datetime) -> str:
        """
        Formata um objeto datetime para string no padrão DD/MM/AAAA.
        Ex: 2023-12-25 -> '25/12/2023'
        """
        if not date_obj:
            return ""
        # strftime = String Format Time
        return date_obj.strftime("%d/%m/%Y")
        
    @staticmethod
    def format_cpf(cpf: str) -> str:
        """
        Aplica a máscara de CPF visualmente: 000.000.000-00.
        Assume que o CPF já tem 11 dígitos (validado pelo CpfValidator).
        """
        if not cpf or len(cpf) != 11:
            return cpf
            
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"