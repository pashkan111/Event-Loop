import selectors, time
from awaitables import Task
from typing import Set


class EventLoop:
    _selector = selectors.DefaultSelector()
    _tasks: Set[Task] = set()
    
    @property
    def selector(self):
        return self._selector

    @property
    def tasks_count(self):
        return len(self._tasks)
    
    def create_task(self, task: Task):
        self._tasks.add(task)
    
    def delete_task(self):
        tasks = self._tasks.copy()
        for task in tasks:
            if task.is_done:
                self._tasks.remove(task)
    
    def run(self):
        while self._tasks:
            events = self._selector.select()
            for selector, event_mask in events:
                data = selector.data
                data()
            self.delete_task()
        self._selector.close()
            
_GlobalEventLoop = EventLoop()


def get_event_loop():
    return _GlobalEventLoop