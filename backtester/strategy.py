#PYTHON
from abc import ABCMeta, abstractmethod

#PROJECT
from event import (
    MarketEvent,
    SignalEvent
)


class StrategyMetaclass(metaclass=ABCMeta):
    @abstractmethod
    def calculate_signals(self):
        raise NotImplementedError


class BuyAndHoldStrategy(StrategyMetaclass):
    def __init__(
        self,
        data,
        event_queue
    ):
    self.data = data
    self.symbol_list = self.data.symbol_list
    self.event_queue = event_queue
    self.bought = {symbol: False for symbol in self.symbol_list}

    def calculate_signals(self, event):
        if isinstance(event, MarketEvent):
            for symbol in self.symbol_list:
                data = self.data.get_latest_data(symbol)[0]
                if data is not None and len(data) > 0:
                    signal = SignalEvent(
                        symbol,
                        data[1],
                        'LONG'
                    )
                    self.event_queue.put(signal)
                    self.bought[symbol] = True
