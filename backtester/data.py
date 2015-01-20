#PYTHON
from abc import ABCMeta, abstractmethod


class DataMetaclass(metaclass=ABCMeta):
    @abstractmethod
    def get_latest_bars(self, symbol, quantity):
        raise NotImplementedError

    @abstractmethod
    def update_bars(self):
        raise NotImplementedError
