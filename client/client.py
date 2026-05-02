from broker import MemoryBroker
from task import Task,TaskStatus
from uuid import UUID


class Client:
    def __init__(self, broker: MemoryBroker):
        self.broker: MemoryBroker = broker

    async def send(self,function_name: str, *args, **kwargs) -> Task:
        task = Task(function_name,args,kwargs)
        await self.broker.put(task)
        return task


    def get_result(self,task_id: UUID | str) -> TaskStatus:
        return self.broker.tasks[task_id]
