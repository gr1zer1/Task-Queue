from abc import ABC, abstractmethod
from task import Task

from uuid import UUID

class BaseBroker(ABC):
    @abstractmethod
    async def put(self, task:Task): ...
    
    @abstractmethod
    async def get(self) -> Task: ...
    
    @abstractmethod
    def done(self): ...

    @abstractmethod
    async def get_by_id(self,id: str|UUID) -> Task: ...

    @abstractmethod
    async def set_by_id(self,task:Task): ...