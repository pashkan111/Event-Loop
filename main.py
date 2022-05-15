from loop import get_event_loop
from awaitebles import Task
from http_client import Client


def main():
    client = Client()
    yield from client.get('http://localhost:8089/time')
    


if __name__ == '__main__':
    
    loop = get_event_loop()
    loop.create_task(Task(main()))
    
    loop.run()