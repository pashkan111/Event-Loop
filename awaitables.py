from typing import Callable, Generator


class Future:
    _done = False
    
    def __init__(self):
        self._callbacks = []
        self._result = None

    @property
    def is_done(self):
        return self._done
        
    @property
    def result(self):
        return self._result
        
    def set_result(self, value):
        self._result = value
        self._done = True
        for cb in self._callbacks:
            cb(self)
    
    def add_callback(self, cb: Callable):
        self._callbacks.append(cb)
    
    def __iter__(self):
        yield self
        return self._result


class Task(Future):
    def __init__(self, coro: Generator):
        super().__init__()
        self._coro = coro
        f = Future()
        f.set_result(None)
        self.step(f)

    def step(self, future: Future):
        try:
            future_new = self._coro.send(future.result)
        except StopIteration:
            self.set_result(future.result)
            return
        future_new.add_callback(self.step)