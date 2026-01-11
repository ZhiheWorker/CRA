import asyncio
from .async_server import AsyncServer

async def main():
    server = AsyncServer("localhost", 8888)
    await server.start()

if __name__ == "__main__":
    asyncio.run(main())