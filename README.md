#quantstart-backtester

This repository is a **hand-written (no copying and pasting here, noob!)**, slightly modified code, of an ~~eight~~seven-part* article series written by [Michael Halls-Moore](http://www.quantstart.com/about-mike/), "the guy behind QuantStart.com":

1. [Event-Driven Backtesting with Python - Part I](http://www.quantstart.com/articles/Event-Driven-Backtesting-with-Python-Part-I)
2. [Event-Driven Backtesting with Python - Part II](http://www.quantstart.com/articles/Event-Driven-Backtesting-with-Python-Part-II)
3. [Event-Driven Backtesting with Python - Part III](http://www.quantstart.com/articles/Event-Driven-Backtesting-with-Python-Part-III)
4. [Event-Driven Backtesting with Python - Part IV](http://www.quantstart.com/articles/Event-Driven-Backtesting-with-Python-Part-IV)
5. [Event-Driven Backtesting with Python - Part V](http://www.quantstart.com/articles/Event-Driven-Backtesting-with-Python-Part-V)
6. [Event-Driven Backtesting with Python - Part VI](http://www.quantstart.com/articles/Event-Driven-Backtesting-with-Python-Part-VI)
7. [Event-Driven Backtesting with Python - Part VII](http://www.quantstart.com/articles/Event-Driven-Backtesting-with-Python-Part-VII)
8. [Event-Driven Backtesting with Python - Part VIII](http://www.quantstart.com/articles/Event-Driven-Backtesting-with-Python-Part-VIII)

###Purpose
I wanted to put together the code from the articles to better understand the event-based part of the code. The basic logic of the event-base is:

1. `update_data()` puts a `MarketEvent()` into the queue
2. `calculate_signals()` processes the `MarketEvent()` and puts a `SignalEvent()` into the queue
3. `update_signal()` processes an `OrderEvent()`
4. `execute_order()` puts a `FillEvent()` into the queue
5. `update_fill()` emits NO event so queue is Empty which breaks inner While loop
6. return to outer While loop
7. continue looping until `data.continue_backtest == False`, at which time loop will end after next `MarketEvent()`

###Notes
1. I say ~~eight~~seven-part article series because Part VIII is specifically for corresponding with Interactive Broker's API, which is beyond the scope of the academic exercise this repository represents.
2. It is important to note the aggregate of the code **as-is** from the series **does not work**. The code has missing logic and minor variable naming mismatches.
3. I tried to keep my variable/method naming conventions **very** similar to their originals so one can more easily compare my code to the articles
4. I took the liberty to make many minor logic changes (e.g. QuantStart's `Portfolio()` has `dict((k,v) for k, v in [(s, 0) for s in self.symbol_list]))` and I have `{symbol: 0 for symbol in self.symbol_list}`
5. The QuantStart code is full of opportunities for DRY improvements, some of which I made and plenty more I left alone
