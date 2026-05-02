from abc import ABC, abstractmethod
from task import Task

class BaseBroker(ABC):
    @abstractmethod
    async def put(self, task:Task): ...
    
    @abstractmethod
    async def get(self): ...
    
    @abstractmethod
    def done(self): ...