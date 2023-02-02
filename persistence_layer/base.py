from abc import abstractmethod, ABC


class PersistenceLayer(ABC):
    @abstractmethod
    def add(self, data):
        ...

    @abstractmethod
    def select(self,):
        ...

    @abstractmethod
    def delete(self, bookmark_id: int):
        ...

    @abstractmethod
    def edit(self, bookmark_id: int, bookmark_data):
        ...
