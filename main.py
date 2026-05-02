from broker import MemoryBroker
from client import Client
from worker import Worker
from registry import func_registry,task
from task import TaskStatus
import asyncio


event = asyncio.Event()

broker = MemoryBroker()
client = Client(broker)
worker = Worker(broker,func_registry)

@task
async def add(a,b):
    return a+b


async def main():

    worker_task = asyncio.create_task(worker.run())
    task_ = await client.send("add", 12, 15)
    
    await task_.event.wait()

    worker_task.cancel()

    print(broker.tasks[task_.id].result)


asyncio.run(main())

