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
        bars,
        event_queue
    ):
    self.bars = bars
    self.symbol_list = self.bars.symbol_list
    self.event_queue = event_queue
    self.bought = {symbol: False for symbol in self.symbol_list}

    def calculate_signals(self, event):
        if isinstance(event, MarketEvent):
            for symbol in self.symbol_list:
                bar = self.bars.get_latest_bars(symbol)[0]
                if bars is not None and len(bars) > 0:
                    signal = SignalEvent(
                        symbol,
                        bar[1],
                        'LONG'
                    )
                    self.event_queue.put(signal)
                    self.bought[symbol] = True
