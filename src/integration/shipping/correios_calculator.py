from .shipping_calculator import ShippingCalculator

class CorreiosCalculator(ShippingCalculator):
    def calcular(self, cep_destino: str, peso_total: float) -> float:
        # Simulação: Taxa fixa R$ 15.00 + R$ 2.00 por kg
        custo = 15.00 + (peso_total * 2.00)
        return round(custo, 2)