from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional
from src.config.database import DatabaseConnection

T = TypeVar('T')

class BaseRepository(ABC, Generic[T]):
    """
    Classe Abstrata Base para repositórios.
    """
    
    def __init__(self):
        # 1. Cria a conexão do jeito novo
        self.db = DatabaseConnection()
        
        # 2. --- HACK DE COMPATIBILIDADE ---
        # Cria um apelido para que o código do seu amigo (que chama _conn_factory)
        # seja redirecionado para a função certa (get_connection).
        self._conn_factory = self.db.get_connection

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