"""starts and implements server logic"""
import asyncio
from pathlib import Path
from hashlib import md5
from asyncio.streams import StreamReader, StreamWriter

import csv

import os

# Changed Dir so that it can be run from anywhere
os.chdir(Path(__file__).resolve().parent)

# Will store all Clients
clients = []
with open(Path('./clients.csv').resolve()) as client_info:
    for [_client, _passwd, _cwd] in csv.reader(client_info):
        clients.append([_client, _passwd, Path(_cwd), False])


def position_of_client_in_clients(target_client):
    """Will position of specified client"""
    for i in range(len(clients)):
        if clients[i][0] == target_client:
            return i + 1
    return False


def login(info, arguments):
    """Login Command Implementation."""
    arguments = arguments.split(' ', 1)
    if len(arguments) != 2:
        return 'Invalid Command'

    position = position_of_client_in_clients(arguments[0])

    if not position:
        return 'Client Not Exist'

    if md5(arguments[1].encode()).hexdigest() == clients[position - 1][1]:
        if clients[position - 1][3]:
            return 'User Already Logged In'

        if info['client']:
            pstn = position_of_client_in_clients(info['client'])
            clients[pstn - 1][3] = False

        info['client'] = arguments[0]
        clients[position-1][3] = True

        return f'Logged In as {info["client"]}'
    return 'Invalid Password'


def register(info, args):
    """Register Command Implementation"""
    arguments = args.split(' ', 1)
    if len(arguments) != 2:
        return 'Invalid Command'

    position = position_of_client_in_clients(arguments[0])

    if position:
        return 'Client Exist'

    client_dir = Path(f'./client_dirs/{arguments[0]}').resolve()
    client_dir.mkdir(parents=True)

    md5_hash = md5(arguments[1].encode()).hexdigest()

    with open('./clients.csv', 'a') as client_info:
        client_info.write(f'{arguments[0]},{md5_hash},{client_dir}\n')

    clients.append([arguments[0], md5_hash, client_dir, False])
    return 'Account Succesfuly Created\nLogin Using "login <client> <passwd>"'


def commands():
    """For Showing Help"""
    return Path('./help.txt').read_text()


def lst(info):
    """List Command Implementation"""
    position = position_of_client_in_clients(info['client'])
    client_dir = clients[position-1][2]
    return str([x.name for x in client_dir.iterdir()])


def create_folder(info, arguments):
    """Create Folder Command Implementation"""
    position = position_of_client_in_clients(info['client'])
    client_dir = clients[position-1][2]
    create: Path = client_dir / arguments
    if create.exists():
        return 'Already Exist'
    create.mkdir(parents=True)
    return f'Created {arguments}'


def change_folder(info, arguments):
    """Change Folder Command Implementation"""
    position = position_of_client_in_clients(info['client'])
    client_dir = clients[position-1][2]
    change: Path = (client_dir / arguments).resolve()
    if not change.exists() and change.is_dir():
        return 'Directory not Exist'
    if not info['client'] in str(change.resolve()):
        return 'Out of Scope'
    client_dir = clients[position-1][2] = change
    return f'Changed to {arguments}'


def read_file(info, arguments):
    """Read File Command Implementation"""
    position = position_of_client_in_clients(info['client'])
    client_dir = clients[position-1][2]
    file: Path = client_dir / arguments
    if file.exists() and file.is_file():
        return file.read_text()
    return 'File Not Exist'


def write_file(info, arguments):
    """Write File Command Implementation"""
    arguments = arguments.split(' ', 1)
    if len(arguments) != 2:
        return 'Invalid Command'
    position = position_of_client_in_clients(info['client'])
    client_dir = clients[position-1][2]
    file: Path = client_dir / arguments[0]
    with open(file, 'a') as f:
        f.write(arguments[1])
    return 'Done Writing'


async def server_logic(reader: StreamReader, writer: StreamWriter):
    """Server Handler"""
    login_message = '''You are not logged in, Login/Register to Continue.
use \'commands\' for getting help.'''
    writer.write((login_message + '\n# ').encode())

    info = {
        'client': ''
    }

    while True:
        message = await reader.read(512)
        message = message.decode()

        if message == 'quit':
            if info['client']:
                position = position_of_client_in_clients(info['client'])
                clients[position - 1][3] = False
            break

        result = "Invalid Command"

        if message.startswith('login '):
            result = login(info, message[6:])
        elif message.startswith('register '):
            result = register(info, message[9:])
        elif message == 'commands':
            result = commands()
        elif not info['client']:
            result = login_message
        elif message == 'list':
            result = lst(info)
        elif message.startswith('change_folder '):
            result = change_folder(info, message[14:])
        elif message.startswith('read_file '):
            result = read_file(info, message[10:])
        elif message.startswith('write_file '):
            result = write_file(info, message[11:])
        elif message.startswith('create_folder '):
            result = create_folder(info, message[14:])

        prompt = f'{info["client"]}' if info['client'] else '#'

        result += f'\n{prompt} '

        writer.write(result.encode())

    writer.close()


async def server():
    """Server Runner"""
    _server = await asyncio.start_server(server_logic, '127.0.0.1', 8088)
    async with _server:
        await _server.serve_forever()

if __name__ == '__main__':
    asyncio.run(server())
