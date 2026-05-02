from broker import MemoryBroker
from client import Client
from worker import Worker
from registry import func_registry,task
import asyncio


event = asyncio.Event()

broker = MemoryBroker()
client = Client(broker)
worker = Worker(broker,func_registry)

@task(broker=broker)
async def add(a,b):
    return a+b


async def main():
    worker_task = asyncio.create_task(worker.run())
    results = await asyncio.gather(
        add.run(1, 2),
        add.run(3, 4),
        add.run(5, 6),

    )
    for res in results:
        await res.event.wait()
        print(res.result)
    worker_task.cancel()

asyncio.run(main())



