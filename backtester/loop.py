#PYTHON
import Queue
import time

#PROJECT
from .events import (
    MarketEvent,
    SignalEvent,
    OrderEvent,
    FillEvent
)
from .data import HistoricCSVDataHandler
from .strategy import BuyAndHoldStrategy
from .portfolio import Portfolio
from .broker import ExecutionHandler

#MODULE
events = Queue.Queue()
data = HistoricCSVDataHandler()
strategy = BuyAndHoldStrategy()
portfolio = Portfolio()
broker = ExecutionHandler()

while True:
    if data.continue_backtest is True:
        data.update_latest_data()
    else:
        break

    while True:
        try:
            event = events.get(block=False)
        except Queue.Empty:
            break

        if event is not None:
            if isinstance(event, MarketEvent):
                strategy.calculate_signals(event)
                portfolio.update_timeindex(event)
            elif isinstance(event, SignalEvent):
                portfolio.update_signal(event)
            elif isinstance(event, OrderEvent):
                broker.execute_order(event)
            elif isinstance(event, FillEvent):
                portfolio.update_fill(event)

    time.sleep(10*60)
