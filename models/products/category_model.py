class Categoria:
    """
    Representa uma categoria de produtos na loja (ex: Hardware, Periféricos).
    Serve para agrupar e filtrar produtos.
    """

    def __init__(self, nome: str, id: int = None):
        """
        Construtor da Categoria.
        :param nome: Nome da categoria (ex: 'Placas de Vídeo')
        :param id: Identificador único do banco (opcional na criação)
        """
        self._id = id
        self.nome = nome

    @property
    def id(self):
        """Getter do ID (somente leitura)"""
        return self._id

    def __str__(self):
        return self.nome

    def __repr__(self):
        return f"<Categoria: {self.nome} (ID: {self._id})>"