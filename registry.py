from task import Task,TaskFunc
from broker import MemoryBroker


func_registry:dict = dict()

def task(broker: MemoryBroker):
    def decorator(func):
        func_registry[func.__name__] = func
        return TaskFunc(func=func, broker=broker)
    return decorator