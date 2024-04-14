"""starts and implements client logic"""
import asyncio
from asyncio.streams import StreamReader, StreamWriter


async def client_logic(reader: StreamReader, writer: StreamWriter):
    """Client Handler"""
    while True:
        message = await reader.read(512)
        message = message.decode()

        print(message, end='')

        message = input()
        writer.write(message.encode())

        if message == 'quit':
            break

    writer.close()


async def client():
    """Client Connector"""
    reader, writer = await asyncio.open_connection('127.0.0.1', 8088)
    await client_logic(reader, writer)


asyncio.run(client())
