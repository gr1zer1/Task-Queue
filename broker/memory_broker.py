from asyncio import Queue
from task import Task
from .broker import BaseBroker
import uuid


class MemoryBroker(BaseBroker):

    def __init__(self):
        self.queue: Queue[Task] = Queue()
        self.tasks: dict[uuid.UUID,Task] = dict()

    
    async def put(self,task:Task):
        await self.queue.put(task)
        self.tasks[task.id] = task
    
    async def get(self):
        return await self.queue.get()
    
    def done(self):
        self.queue.task_done()