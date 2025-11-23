from src.models.products.category_model import Categoria
# Importa o validador que você criou na task anterior
from utils.validators.price_validator import PriceValidator

class Produto:
    """
    Representa um item físico vendável no sistema.
    Possui relacionamento com Categoria e validações financeiras.
    """

    def __init__(self, nome: str, sku: str, preco: float, categoria: Categoria, estoque: int = 0, id: int = None):
        """
        :param nome: Título do produto
        :param sku: Código único (Stock Keeping Unit)
        :param preco: Valor unitário (validado)
        :param categoria: Objeto da classe Categoria (Agregação)
        :param estoque: Quantidade inicial (validado)
        """
        self._id = id
        self.nome = nome
        self.sku = sku
        self.categoria = categoria  # O produto 'tem uma' categoria
        
        # Atributos protegidos
        self._preco = 0.0
        self._estoque = 0
        
        # Usa os setters para validar na inicialização
        self.preco = preco
        self.estoque = estoque

    @property
    def id(self):
        return self._id

    @property
    def preco(self):
        return self._preco

    @preco.setter
    def preco(self, valor: float):
        # Validação usando a classe utilitária
        if not PriceValidator.validate_price(valor):
            raise ValueError(f"Preço inválido para o produto '{self.nome}': {valor}")
        self._preco = valor

    @property
    def estoque(self):
        return self._estoque

    @estoque.setter
    def estoque(self, valor: int):
        if not PriceValidator.validate_stock(valor):
            raise ValueError(f"Estoque inválido: {valor}")
        self._estoque = valor

    def tem_estoque(self, quantidade: int = 1) -> bool:
        """Verifica se há quantidade suficiente para venda."""
        return self.estoque >= quantidade

    def __str__(self):
        return f"{self.nome} - R$ {self.preco:.2f}"