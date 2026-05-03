from broker import BaseBroker
from task import Task
from uuid import UUID
from registry import func_registry


class Client:
    def __init__(self, broker: BaseBroker):
        self.broker: BaseBroker = broker

    async def send(self, func_id: str, *args, **kwargs) -> Task:
        function = func_registry[func_id]
        task = Task(function, args, kwargs, func_id=func_id, func_name=function.__name__)
        await self.broker.set_by_id(task)
        await self.broker.put(task)
        return task


    async def get_result(self,task_id: UUID | str) -> Task:
        return await self.broker.get_by_id(task_id)
