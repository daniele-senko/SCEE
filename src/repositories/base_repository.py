from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional
from src.config.database import DatabaseConnection

# T representa um Objeto de Modelo (ex: Usuario, Produto)
T = TypeVar('T')

class BaseRepository(ABC, Generic[T]):
    """
    Classe Abstrata Base para repositórios.
    Gerencia a conexão com o SQLite usando o padrão Singleton.
    """
    
    def __init__(self):
        # CORREÇÃO AQUI: Não pedimos argumentos, pegamos a instância direto
        self.db = DatabaseConnection()
    
    def _get_connection(self):
        """Helper para pegar a conexão do singleton"""
        return self.db.get_connection()

    @abstractmethod
    def salvar(self, obj: T) -> T:
        pass
    
    @abstractmethod
    def buscar_por_id(self, id: int) -> Optional[T]:
        pass
    
    @abstractmethod
    def listar(self) -> List[T]:
        pass
    
    @abstractmethod
    def deletar(self, id: int) -> bool:
        pass