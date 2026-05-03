import uuid
from typing import Any,Callable
from enum import StrEnum
from asyncio import Event
import json
from dataclasses import dataclass

from registry import func_registry

import dataclasses


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



@dataclass
class TaskMessage:
    id:str
    args:Any
    kwargs:Any
    result: None|Any
    status:str

    def to_json(self) -> str:
        return json.dumps(dataclasses.asdict(self))
    
    @classmethod
    def from_json(cls,data:str|bytes):
        task = json.loads(data)
        return cls(**task)


    def to_task(self) -> Task:
        task = Task(func_registry[self.id],self.args,self.kwargs)

        task.id = uuid.UUID(self.id)
        task.result = self.result
        task.status = self.status
        return task

    @classmethod
    def from_task(cls,task:Task):
        func_registry[str(task.id)] = task.function
        return TaskMessage(
            id=str(task.id),
            args = task.args,
            kwargs=task.kwargs,
            result=task.result,
            status=str(task.status)
            )
