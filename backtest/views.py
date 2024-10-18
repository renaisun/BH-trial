import os

from rest_framework.decorators import api_view
from rest_framework.response import Response

from backtest.util.backtest import backtest
from fetch_data.models import DailyStockPrice


# Create your views here.

@api_view(['GET'])
def get_back_rest_result(request):
    # get the stock symbol from the request parameters
    stock_symbol = request.GET.get('symbol')

    # retrieve the initial investment amount from the request
    initial_invest_amount = request.GET.get('initial_invest_amount')

    # get the short window period for the moving average
    short_window = request.GET.get('short_window')

    # get the long window period for the moving average
    long_window = request.GET.get('long_window')

    # check missing parameters
    param_missing = []
    params = ["symbol", "initial_invest_amount", "short_window", "long_window"]
    for param in params:
        if request.GET.get(param) is None:
            param_missing.append(param)
    if len(param_missing) > 0:
        return Response({"msg": f"Missing parameters: {', '.join(param_missing)}"}, status=400)

    history = DailyStockPrice.objects.filter(stock_symbol=stock_symbol).order_by('date').values()

    initial_invest_amount, short_window, long_window = float(initial_invest_amount), int(short_window), int(long_window)
    result = backtest(initial_invest_amount, short_window, long_window, history)

    return Response({"msg": result})
