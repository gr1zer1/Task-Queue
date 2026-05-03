from __future__ import annotations
from typing import Callable,TYPE_CHECKING
from . import Task
from registry import func_registry


if TYPE_CHECKING:
    from broker import BaseBroker

class TaskFunc:
    
    def __init__(self, func: Callable, broker: BaseBroker):
        self.func: Callable = func
        self.broker = broker
    

    async def run(self,*args,**kwargs):
        task = Task(self.func,args,kwargs)
        await self.broker.set_by_id(task)
        await self.broker.put(task)
        return task
    




def task(broker: BaseBroker):
    def decorator(func):
        func_registry[func.__name__] = func
        return TaskFunc(func=func, broker=broker)
    return decorator