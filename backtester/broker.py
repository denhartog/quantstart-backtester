#PYTHON
from abc import (
    ABCMeta,
    abstractmethod
)
from datetime import date

#PROJECT
from .events import (
    OrderEvent,
    FillEvent
)

class BrokerMetaclass(metaclass=ABCMeta):
    @abstractmethod
    def execute_order(self, event):
        raise NotImplementedError


class BacktestBroker(BrokerMetaclass):
    def __init__(self, event_queue):
        self.event_queue = event_queue

    def execute_order(self, event):
        """Converts OrderEvents into FillEvents"""
        if isinstance(event, OrderEvent):
            signal = FillEvent(
                event.symbol,
                date.today(),
                event.quantity,
                event.direction,
                None
            )
            self.event_queue.put(signal)
