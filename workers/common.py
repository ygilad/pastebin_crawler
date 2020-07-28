import abc
import queue
import threading


class WorkerThreadBase(threading.Thread, metaclass=abc.ABCMeta):
    """ A base for worker thread that will allow extending classes easy access to tasks via in & out queues

        Ask the thread to stop by calling its join() method.
    """

    def __init__(self, in_q=None, out_q=None, reccurence_interval=None):
        super(WorkerThreadBase, self).__init__()
        self._in_q = in_q
        self._out_q = out_q
        self._stop_request = threading.Event()
        self._reccurence_interval = reccurence_interval

    def run(self):
        # pooling for tasks in the queue, run forever or until called calls join()
        while not self._stop_request.isSet():
            try:
                task = self._in_q.get(True, 0.05)
                res = self.perform(task)
                if res and self._out_q is not None:
                    self._out_q.put(res)
            except queue.Empty:
                continue

    def join(self, timeout=None):
        self._stop_request.set()
        super(WorkerThreadBase, self).join(timeout)

    @abc.abstractmethod
    def perform(self, task):
        pass
