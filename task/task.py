import uuid
from typing import Any,Callable
from enum import StrEnum
from asyncio import Event


class TaskStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    DONE = "done"
    FAILED = "failed"


class Task:
    def __init__(self, function: Callable, args, kwargs):
        """
        status = pending(by default), running, done, failed
        """
        self.id: uuid.UUID = uuid.uuid4()
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.result: None | Any = None 
        self.status: TaskStatus = TaskStatus.PENDING
        self.event = Event()


