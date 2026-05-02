from asyncio import Queue
from task import Task

class MemoryBroker:

    def __init__(self):
        self.queue: Queue[Task] = Queue()

    
    async def put(self,task:Task):
        await self.queue.put(task)
    
    async def get(self):
        return await self.queue.get()
    
    def done(self):
        self.queue.task_done()