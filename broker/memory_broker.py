from asyncio import Queue
from task import Task
from .broker import BaseBroker
import uuid


class MemoryBroker(BaseBroker):

    def __init__(self):
        self.queue: Queue[Task] = Queue()
        self.tasks: dict[str,Task] = dict()

    
    async def put(self,task:Task):
        await self.queue.put(task)
        self.tasks[str(task.id)] = task
    
    async def get(self):
        return await self.queue.get()
    
    def done(self):
        self.queue.task_done()

    
    async def set_by_id(self, task:Task):
        self.tasks[str(task.id)] = task
    

    async def get_by_id(self, id:str | uuid.UUID):
        task = self.tasks.get(str(id))
        if task is None: raise Exception
        else: return task
