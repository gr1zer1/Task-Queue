import uuid
from typing import Any, Callable
from enum import StrEnum
from asyncio import Event
import json
from dataclasses import dataclass

from registry import func_registry

import dataclasses


def default_func_id(function: Callable) -> str:
    return f"{function.__module__}.{function.__qualname__}"


class TaskStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    DONE = "done"
    FAILED = "failed"


class Task:
    def __init__(
        self,
        function: Callable,
        args,
        kwargs,
        func_id: str | None = None,
        func_name: str | None = None,
    ):
        """
        status = pending(by default), running, done, failed
        """
        self.id: uuid.UUID = uuid.uuid4()
        self.function = function
        self.func_id = func_id or default_func_id(function)
        self.func_name = func_name or function.__name__
        self.args = args
        self.kwargs = kwargs
        self.result: None | Any = None 
        self.status: TaskStatus = TaskStatus.PENDING
        self.event = Event()



@dataclass
class TaskMessage:
    id: str
    func_id: str
    func_name: str
    args: Any
    kwargs: Any
    result: None | Any
    status: str

    def to_json(self) -> str:
        return json.dumps(dataclasses.asdict(self))
    
    @classmethod
    def from_json(cls, data: str | bytes):
        task = json.loads(data)
        if "func_id" not in task:
            if len(func_registry) != 1:
                raise KeyError("Task message has no func_id and function registry is ambiguous")
            func_id, function = next(iter(func_registry.items()))
            task["func_id"] = func_id
            task["func_name"] = function.__name__
        return cls(**task)


    def to_task(self) -> Task:
        task = Task(
            func_registry[self.func_id],
            self.args,
            self.kwargs,
            func_id=self.func_id,
            func_name=self.func_name,
        )

        task.id = uuid.UUID(self.id)
        task.result = self.result
        task.status = TaskStatus(self.status)
        return task

    @classmethod
    def from_task(cls, task: Task):
        return TaskMessage(
            id=str(task.id),
            func_id=task.func_id,
            func_name=task.func_name,
            args=task.args,
            kwargs=task.kwargs,
            result=task.result,
            status=str(task.status)
        )
