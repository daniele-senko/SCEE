from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional
from src.config.database import DatabaseConnection

T = TypeVar('T')

class BaseRepository(ABC, Generic[T]):
    """
    Classe Abstrata Base para repositórios.
    """
    
    def __init__(self):
        self.db = DatabaseConnection()
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

    # --- MÉTODOS DE TRANSAÇÃO CORRIGIDOS ---
    # Removemos o .close() para não matar a conexão compartilhada da aplicação.
    
    def iniciar_transacao(self):
        """Retorna a conexão para controle manual."""
        return self._conn_factory()

    def commit_transacao(self, conexao):
        """Confirma as alterações."""
        if conexao:
            conexao.commit()
            # conexao.close()  <-- REMOVIDO: Não feche a conexão se ela for compartilhada!

    def rollback_transacao(self, conexao):
        """Reverte as alterações."""
        if conexao:
            try:
                conexao.rollback()
            except Exception:
                pass
            # conexao.close()  <-- REMOVIDO