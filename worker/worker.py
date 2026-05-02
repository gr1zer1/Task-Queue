from broker import MemoryBroker
from registry import func_registry
from task import TaskStatus


class Worker:
    def __init__(self, broker:MemoryBroker, registry:dict):
        self.broker = broker
        self.registry = registry
    

    async def run(self):
        while True:
            task = await self.broker.get()
            task.status = TaskStatus.RUNNING
            try:
                func = self.registry[task.function_name]
                task.result = await func(*task.args,**task.kwargs)

                task.status = TaskStatus.DONE
            
            except Exception as e:
                task.status = TaskStatus.FAILED
                task.result = e

            self.broker.done()

            