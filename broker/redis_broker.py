from .broker import BaseBroker
import socket
import asyncio
from urllib.parse import urlparse
from task import Task,TaskMessage

from uuid import UUID

from redis import encode_command,decode_response


class RedisBroker(BaseBroker):

    def __init__(self,url:str):
        self._socket: socket.socket | None = None
        self._loop: asyncio.AbstractEventLoop | None = None
        self._lock = asyncio.Lock()
        parsed_url = urlparse(url)
        self.host = parsed_url.hostname
        self.port = parsed_url.port

        if self.host == None or self.port == None:
            raise Exception 
        

    
    async def connect(self):
        self._loop = asyncio.get_event_loop()

        try:
            infos = await self._loop.getaddrinfo(self.host,self.port,type=socket.SOCK_STREAM)
        except:
            raise Exception
        
        if not infos:
            raise Exception
        

        family, socktype, proto, canonname, sockaddr = infos[0]

        self._socket = socket.socket(family,socktype,proto)
        self._socket.setblocking(False)

        try:
            await asyncio.wait_for(
                self._loop.sock_connect(self._socket,sockaddr),
                timeout=10.0
            )
        except:
            raise Exception
        
    async def _send(self, data:bytes):
        await self._loop.sock_sendall(self._socket,data)
    
    async def _recv(self) -> bytes:
        buffer = b""
        while True:
            buffer += await self._loop.sock_recv(self._socket, 4096)
            try:
                decode_response(buffer)
                return buffer
            except:
                continue
    
    def close(self):
        self._socket.close()
        self._socket = None


    async def put(self, task:Task):
        async with self._lock:
            task_message = TaskMessage.from_task(task)
            json_str = task_message.to_json()
            await self._send(encode_command("LPUSH","tasks",json_str))
            await self._recv()

        return task_message

    
    async def get(self) -> Task:
        async with self._lock:
            await self._send(encode_command("BRPOP", "tasks", "0"))
            parsed = decode_response(await self._recv())
            return TaskMessage.from_json(parsed[1]).to_task()
    

    def done(self):
        pass


    async def get_by_id(self,id: UUID | str):
        async with self._lock:
            await self._send(encode_command("GET",f"task:{str(id)}"))
            res = await self._recv()
            task_message = TaskMessage.from_json(decode_response(res))

        task = task_message.to_task()

        return task


    async def set_by_id(self,task:Task):
        async with self._lock:
            task_json = TaskMessage.from_task(task).to_json()
            await self._send(encode_command("SET",f"task:{str(task.id)}",task_json))
            await self._recv()

        return task_json
    
