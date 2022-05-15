from loop import get_event_loop
from awaitables import Task
from http_client import Client


def make_request():
    results = []
    for _ in range(100):
        client = Client()
        yield from client.get('https://soccer365.ru/games/1563678/')


def main():
    results = []
    yield from make_request


if __name__ == '__main__':
    
    loop = get_event_loop()
    loop.create_task(Task(main()))
    
    loop.run()