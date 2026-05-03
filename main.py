from broker import RedisBroker
from worker import Worker
from registry import func_registry
import asyncio
from task import TaskStatus, task



broker = RedisBroker("redis://localhost:6379")
worker_broker = RedisBroker("redis://localhost:6379")
worker = Worker(worker_broker, func_registry)

@task(broker=broker)
async def add(a,b):
    return a+b


async def main():
    await broker.connect()

    worker_task = asyncio.create_task(worker.run())
    tasks = await asyncio.gather(
        add.run(1, 2),
        add.run(3, 4),
        add.run(5, 6),

    )
    for task_result in tasks:
        while True:
            saved_task = await broker.get_by_id(task_result.id)
            if saved_task.status in (TaskStatus.DONE, TaskStatus.FAILED):
                print(saved_task.result)
                break
            await asyncio.sleep(0.1)

    worker_task.cancel()

asyncio.run(main())


