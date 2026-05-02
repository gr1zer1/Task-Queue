from __future__ import annotations
from typing import Callable,TYPE_CHECKING
from . import Task


if TYPE_CHECKING:
    from broker import MemoryBroker

class TaskFunc:
    
    def __init__(self, func: Callable, broker: MemoryBroker):
        self.func: Callable = func
        self.broker = broker
    

    async def run(self,*args,**kwargs):
        task = Task(self.func,args,kwargs)
        self.broker.tasks[task.id] = task
        await self.broker.put(task)
        return task
    
    