from abc import ABC, abstractmethod

class BaseBroker(ABC):
    @abstractmethod
    async def put(self, task): ...
    
    @abstractmethod
    async def get(self): ...
    
    @abstractmethod
    def done(self): ...