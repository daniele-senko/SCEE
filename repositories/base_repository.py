"""Repositório base abstrato para operações CRUD.

Define a interface padrão que todos os repositórios devem implementar,
seguindo o padrão Repository para abstração de acesso a dados.
"""
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional, Dict, Any

T = TypeVar('T')


class BaseRepository(ABC, Generic[T]):
    """Interface abstrata para repositórios (padrão Repository).
    
    Esta classe define os métodos básicos de CRUD que todos os
    repositórios concretos devem implementar.
    
    Type Parameters:
        T: Tipo do modelo que o repositório manipula
    """
    
    def __init__(self, conn_factory):
        """Inicializa o repositório com uma factory de conexões.
        
        Args:
            conn_factory: Callable que retorna uma conexão com o banco
        """
        self._conn_factory = conn_factory
    
    @abstractmethod
    def salvar(self, obj: T) -> T:
        """Salva um novo registro no banco de dados.
        
        Args:
            obj: Objeto a ser salvo
            
        Returns:
            Objeto salvo com ID atribuído
            
        Raises:
            ValueError: Se os dados forem inválidos
        """
        raise NotImplementedError
    
    @abstractmethod
    def buscar_por_id(self, id: int) -> Optional[T]:
        """Busca um registro por ID.
        
        Args:
            id: ID do registro
            
        Returns:
            Objeto encontrado ou None se não existir
        """
        raise NotImplementedError
    
    @abstractmethod
    def listar(self, limit: Optional[int] = None, offset: int = 0) -> List[T]:
        """Lista todos os registros com paginação opcional.
        
        Args:
            limit: Número máximo de registros a retornar
            offset: Número de registros a pular
            
        Returns:
            Lista de objetos
        """
        raise NotImplementedError
    
    @abstractmethod
    def atualizar(self, obj: T) -> T:
        """Atualiza um registro existente.
        
        Args:
            obj: Objeto com dados atualizados (deve ter ID)
            
        Returns:
            Objeto atualizado
            
        Raises:
            ValueError: Se o objeto não tiver ID ou não existir
        """
        raise NotImplementedError
    
    @abstractmethod
    def deletar(self, id: int) -> bool:
        """Deleta um registro por ID.
        
        Args:
            id: ID do registro a deletar
            
        Returns:
            True se deletado com sucesso, False se não encontrado
        """
        raise NotImplementedError
