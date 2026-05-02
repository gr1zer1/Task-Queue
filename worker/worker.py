from broker import MemoryBroker
from registry import func_registry
from task import TaskStatus
import inspect

class Worker:
    def __init__(self, broker:MemoryBroker, registry:dict):
        self.broker = broker
        self.registry = registry
    

    async def run(self):
        while True:
            task = await self.broker.get()
            task.status = TaskStatus.RUNNING
            try:
                if inspect.iscoroutinefunction(task.function):

                    task.result = await task.function(*task.args,**task.kwargs)
                else:
                    task.result = task.function(*task.args,**task.kwargs)

                task.status = TaskStatus.DONE
            
            except Exception as e:
                task.status = TaskStatus.FAILED
                task.result = e

            self.broker.done()
            task.event.set()


            