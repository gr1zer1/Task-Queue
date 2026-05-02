import uuid
from typing import Any,Callable
from enum import StrEnum
from asyncio import Event
import json
from dataclasses import dataclass

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


    def to_json(self) -> str:
        return json.dumps({
            "id": str(self.id),
            "function": self.function.__name__,
            "args": self.args,
            "kwargs": self.kwargs,
            "status": str(self.status),
        })


@dataclass
class TaskMessage:
    id:str
    function_name:str
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

