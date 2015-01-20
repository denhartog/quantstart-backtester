#PYTHON
from abc import (
    ABCMeta,
    abstractmethod
)


class PortfolioMetaclass(metaclass=ABCMeta):
    @abstractmethod
    def update_signal(self, event):
        raise NotImplementedError

    @abstractmethod
    def update_fill(self, event):
        raise NotImplementedError


class BacktestPortfolio(PortfolioMetaclass):
    def __init__(
        self,
        event_queue,
        data,
        start_date,
        initial_capital
    ):
        self.event_queue = event_queue
        self.data = data
        self.start_date = start_date
        self.initial_capital = initial_capital

        self.symbol_list = self.data.symbol_list

        self.all_positions = self.calculate_all_positions()
        self.current_positions = {symbol: 0 for symbol in self.symbol_list}

        self.all_holdings = self.calculate_all_holdings()
        self.current_holdings = self.calculate_current_holdings()

    def calculate_all_positions(self):
        positions = {symbol: 0 for symbol in self.symbol_list}
        positions['datestamp'] = self.start_date
        return positions

    def calculate_all_holdings(self):
        holdings = {symbol: 0 for symbol in self.symbol_list}
        holdings['datestamp'] = self.start_date
        holdings['cash'] = self.initial_capital
        holdings['commission'] = 0
        holdings['total'] = self.initial_capital
        return holdings

    def calculate_current_holdings(self):
        holdings = {symbol: 0 for symbol in self.symbol_list}
        holdings['cash'] = self.initial_capital
        holdings['commission'] = 0
        holdings['total'] = self.initial_capital
        return holdings

    def update_timeindex(self, event):
        pass

    def update_positions_post_fill(self, event):
        pass

    def update_holdings_post_fill(self, event):
        pass

    def update_fill(self, event):
        pass

    def create_order_event(self, event):
        pass

    def update_signal(self, event):
        pass

    def create_equity_curve_dataframe(self):
        pass
