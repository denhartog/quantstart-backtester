#PACKAGES
import numpy
import pandas


def create_sharpe_ratio(
    returns,
    periods=252
):
    return (
        numpy.sqrt(periods) *
        numpy.mean(returns) /
        numpy.std(returns)
    )


def create_drawdowns(equity_curve):
    high_watermark = [0]
    curve_index = equity_curve.index
    drawdown = pandas.Series(index=curve_index)
    duration = pandas.Series(index=curve_index)

    for i in range(1, len(curve_index)):
        current_high_watermark = max(
            high_watermark[i-1],
            equity_curve[i]
        )
        high_watermark.append(current_high_watermark)

        drawdown[i] = high_watermark[i] - equity_curve[i]
        duration[i] = 0 if drawdown[i] == 0 else duration[i-1] + 1

    return drawdown.max(), duration.max()
