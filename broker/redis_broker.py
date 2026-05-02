from .broker import BaseBroker
import socket
import asyncio
from urllib.parse import urlparse


class RedisBroker(BaseBroker):

    def __init__(self,url:str):
        self._socket: socket.socket | None = None
        self._loop: asyncio.AbstractEventLoop | None = None
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
        
    async def send(self, data:bytes):
        await self._loop.sock_sendall(self._socket,data)
    

    async def recv(self,n:int = 4096) -> bytes:
        return await self._loop.sock_recv(self._socket,n)
    
    def close(self):
        self._socket.close()
        self._socket = None

    
