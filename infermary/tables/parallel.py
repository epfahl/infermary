"""Define process pool context managers and abstract parallel map
implementation.

Notes
-----
* Non-daemonic process implementation adapted from
  https://stackoverflow.com/a/8963618"""

from contextlib import contextmanager
import multiprocessing
from multiprocessing import Process
from multiprocessing.pool import Pool


class NoDaemonProcess(Process):
    """Custom subclass of multiprocessing.Process that is non-daemonic."""

    @property
    def daemon(self):
        return False

    @daemon.setter
    def daemon(self, value):
        pass


class NoDaemonContext(type(multiprocessing.get_context())):
    """Define a non-daemonic process context."""

    Process = NoDaemonProcess


class NDPool(Pool):
    """Define a non-daemonic process pool."""

    def __init__(self, *args, **kwargs):
        kwargs["context"] = NoDaemonContext()
        super(NDPool, self).__init__(*args, **kwargs)


@contextmanager
def create_pool(pool_class, *args, **kwargs):
    """Define a process pool context for the given pool base class and pool
    initialization arguments."""
    pool = pool_class(*args, **kwargs)
    yield pool
    pool.close()
    pool.join()


def map_par(pool_class, map_method="map", chunksize=1):
    """Return a map function for the given pool class, pool args, and map
    chunksize.
    """

    def _map(func, data):
        with create_pool(pool_class) as pool:
            result = getattr(pool, map_method)(func, data, chunksize=chunksize)
        return result

    return _map
