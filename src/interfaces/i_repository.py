from abc import ABC, abstractmethod
from typing import List, Any, Optional

class IRepository(ABC):
    """
    Interface Base (Classe Abstrata) para o padrão Repository.
    Define os métodos CRUD obrigatórios que todas as classes de repositório devem implementar.
    """

    @abstractmethod
    def save(self, entity: Any) -> None:
        """
        Salva (insere ou atualiza) uma entidade no banco de dados.
        :param entity: Objeto da classe de modelo (Ex: Produto, Cliente)
        """
        pass

    @abstractmethod
    def get_by_id(self, entity_id: int) -> Optional[Any]:
        """
        Busca um registro pelo ID único.
        :param entity_id: ID do registro
        :return: Objeto encontrado ou None
        """
        pass

    @abstractmethod
    def get_all(self) -> List[Any]:
        """
        Retorna todos os registros da tabela.
        :return: Lista de objetos
        """
        pass

    @abstractmethod
    def delete(self, entity_id: int) -> None:
        """
        Remove um registro pelo ID.
        :param entity_id: ID do registro a ser removido
        """
        pass