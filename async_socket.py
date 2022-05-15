import socket, selectors
from loop import get_event_loop
from awaitebles import Future


class AsyncSocket:
    def __init__(self):
        self._sock = socket.socket()
        self._sock.setblocking(False)

    def connect(self, host:str, port:int):
        loop = get_event_loop()
        try:
            self._sock.connect((host, port))
        except OSError as e:
            print(e)
        
        future = Future()
            
        def callback():
            loop.selector.unregister(self._sock)
            future.set_result(None)
            print('connected')
            
        loop.selector.register(
            self._sock.fileno(), selectors.EVENT_WRITE, callback
            )
        return (yield from future)

    def send(self, data: str):
        future = Future()
        loop = get_event_loop()
        def callback():
            loop.selector.unregister(self._sock)
            l = self._sock.send(data.encode('utf-8'))
            future.set_result(l)
            print('sent')
            
        loop.selector.register(
            self._sock.fileno(), selectors.EVENT_WRITE, callback
            )
        return (yield from future)
    
    def read(self, count_bytes: int=2000):
        future = Future()
        loop = get_event_loop()

        def callback():
            loop.selector.unregister(self._sock)
            data = self._sock.recv(count_bytes)
            future.set_result(data)

        loop.selector.register(
            self._sock.fileno(), selectors.EVENT_READ, callback
            )
        return (yield from future)
        
    def read_all(self):
        print('read')
        data = bytearray()
        chunk = yield from self.read()
        print(chunk)
        while chunk:
            data.extend(data)
            chunk = yield from self.read()
        return bytes(data)
