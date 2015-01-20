class AbstractEvent:
    pass


class MarketEvent(AbstractEvent):
    pass


class SignalEvent(AbstractEvent):
    def __init__(
        self,
        symbol,
        datestamp,
        signal_type
    ):
        """Initializes a SignalEvent

        signal_type == 'LONG','SHORT'
        """
        self.symbol = symbol
        self.datestamp = datestamp
        self.signal_type = signal_type


class OrderEvent(AbstractEvent):
    def __init__(
        self,
        symbol,
        order_type,
        quantity,
        direction
    ):
        """Initializes an OrderEvent

        order_type == 'MARKET','LIMIT','STOP','STOPLIMT'
        direction == 'BUY','SELL'
        """
        self.symbol = symbol
        self.order_type = order_type
        self.quantity = quantity
        self.direction = direction

    def __repr__(self):
        return '{cls}({d})'.format(
            cls=self.__class__,
            d=self.__dict__
        )


class FillEvent(AbstractEvent):
    def __init__(
        self,
        symbol,
        datestamp,
        quantity,
        direction,
        fill_cost,
        commission=None
    ):
        """Initializes a FillEvent

        direction == 'BUY','SELL'
        commission: is $ per share
        """
        self.symbol = symbol
        self.datestamp = datestamp
        self.quantity = quantity
        self.direction = direction
        self.fill_cost = fill_cost
        self.commission = commission
