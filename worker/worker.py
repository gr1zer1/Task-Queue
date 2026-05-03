from broker import BaseBroker,RedisBroker
from registry import func_registry
from task import TaskStatus, Task
import asyncio

import inspect

class Worker:
    def __init__(self, broker:BaseBroker, registry:dict):
        self.broker = broker
        self.registry = registry
    

    async def run(self):
        if type(self.broker) == RedisBroker:
            await self.broker.connect()
        sem = asyncio.Semaphore(5)
        while True:
            task = await self.broker.get()
            
            asyncio.create_task(self._execute(task,sem))

         
    

    async def _execute(self,task: Task, sem: asyncio.Semaphore):
        async with sem:
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


            