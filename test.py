import asyncio
from broker import RedisBroker
from redis import encode_command, decode_response

async def test():
    broker = RedisBroker("redis://localhost:6379")
    await broker.connect()
    
    await broker._send(encode_command("PING"))
    response = await broker._recv()
    print(decode_response(response))
    
    broker.close()

asyncio.run(test())