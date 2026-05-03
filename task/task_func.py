from __future__ import annotations
from typing import Callable,TYPE_CHECKING
from .task import Task, default_func_id
from registry import func_registry


if TYPE_CHECKING:
    from broker import BaseBroker

class TaskFunc:
    
    def __init__(self, func: Callable, broker: BaseBroker):
        self.func: Callable = func
        self.func_id = default_func_id(func)
        self.func_name = func.__name__
        self.broker = broker
    

    async def run(self,*args,**kwargs):
        task = Task(
            self.func,
            args,
            kwargs,
            func_id=self.func_id,
            func_name=self.func_name,
        )
        await self.broker.set_by_id(task)
        await self.broker.put(task)
        return task
    




def task(broker: BaseBroker):
    def decorator(func):
        func_registry[default_func_id(func)] = func
        return TaskFunc(func=func, broker=broker)
    return decorator
