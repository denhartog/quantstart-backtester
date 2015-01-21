#PYTHON
from abc import (
    ABCMeta,
    abstractmethod
)
from math import copysign

#PROJECT
from .events import (
    SignalEvent,
    OrderEvent
)
from .performance import (
    create_sharpe_ratio,
    create_drawdowns
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
        self.equity_curve = None

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
        data = {
            symbol: self.data.get_latest(data, symbol)
            for symbol in self.symbol_list
        }
        datestamp = data[self.symbol_list[0]][0][1]

        #positions
        positions = {
            symbol: self.current_positions[symbol]
            for symbol in self.symbol_list
        }
        positions['datestamp'] = datestamp
        self.all_positions.append(positions)

        #holdings
        holdings = {symbol: 0 for symbol in self.symbol_list}
        holdings['datestamp'] = datestamp
        holdings['cash'] = self.current_holdings['cash']
        holdings['commission'] = self.current_holdings['commission']
        holdings['total'] = self.current_holdings['cash']

        for symbol in self.symbol_list:
            market_value = self.current_positions[symbol] + data[symbol][0][5]
            holdings[symbol] = market_value
            holdings['total'] += market_value

        self.all_holdings.append(holdings)

    def update_positions_post_fill(self, event):
        direction = 1 if event.direction == 'BUY' else -1
        self.current_positions[event.symbol] += copysign(event.quantity, direction)

    def update_holdings_post_fill(self, event):
        direction = 1 if event.direction == 'BUY' else -1
        fill_cost = self.data.get_latest_data(event.symbol)[0][5]
        cost = copysign(fill_cost, direction) * event.quantity
        self.current_holdings[event.symbol] += cost
        self.current_holdings['cash'] -= cost + event.commission
        self.current_holdings['total'] -= cost + event.commission

    def update_fill(self, event):
        if isinstance(event, FillEvent):
            self.update_positions_post_fill(event)
            self.update_holdings_post_fill(event)

    def create_order_event(self, event):
        if isinstance(event, SignalEvent)
            direction = 'BUY' if event.signal_type == 'LONG' else 'SELL'
            return OrderEvent(
                event.symbol,
                'MARKET',
                100,
                direction
            )

    def update_signal(self, event):
        if isinstance(event, SignalEvent):
            self.event_queue.put(self.create_order_event(event))

    def calculate_equity_curve_dataframe(self):
        curve = pandas.DataFrame(self.all_holdings)
        curve.set_index('datestamp', inplace=True)
        curve['returns'] = curve['total'].pct_change()
        curve['equity_curve'] = (1 + curve['returns']).cumprod()
        self.equity_curve = curve

    def output_summary_stats(self):
        total_return = self.equity_curve['equity_curve'][-1]
        drawdown, duration = create_drawdowns(self.equity_curve['equity_curve'])

        return [
            ('Total return', (total_return - 1) * 100),
            ('Sharpe ratio', create_sharpe_ratio(self.equity_curve['returns'])),
            ('Max drawdown', drawdown * 100),
            ('Drawdown duration', duration)
        ]
