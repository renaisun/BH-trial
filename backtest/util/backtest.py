import pandas as pd

def backtest(initial_invest_amount, short_window, long_window, history_data):
    STATUS_EMPTY, STATUS_BUY, STATUS_SELL = 0, 1, 2
    df = pd.DataFrame(history_data)
    # Calculate moving averages
    df['mean_short'] = df['close_price'].rolling(window=short_window).mean()
    df['mean_long'] = df['close_price'].rolling(window=long_window).mean()
    df['status'] = STATUS_EMPTY
    df.loc[df['close_price'] < df['mean_short'], 'status'] = STATUS_BUY  # buy
    df.loc[df['close_price'] > df['mean_long'], 'status'] = STATUS_SELL  # sell
    stock_count = 0
    money = initial_invest_amount
    trade_history = []
    total_assets = []
    # Iterate through each row in the dataframe to simulate trading
    for idx, row in df.iterrows():
        current_price, status = float(row['close_price']), row['status']
        if status == STATUS_BUY and stock_count == 0:
            qty = money / current_price
            money -= qty * current_price
            stock_count = qty
            trade_history.append({
                "date": row['date'],
                "type": "buy",
                "price": current_price,
                "quantity": qty
            })
        elif status == STATUS_SELL and stock_count > 0:
            money += current_price * stock_count
            trade_history.append({
                "date": row['date'],
                "type": "sell",
                "price": current_price,
                "quantity": stock_count
            })
            stock_count = 0
        total_assets.append(money + stock_count * current_price)

    # calculate total return
    total_return = initial_invest_amount
    if len(total_assets) > 0:
        total_return = (total_assets[-1] - initial_invest_amount) / initial_invest_amount * 100

    # calculate drawdown
    max_drawdown = 0
    peak = 0
    for value in total_assets:
        peak = max(peak, value)
        drawdown = (peak - value) / peak * 100
        max_drawdown = min(max_drawdown, -drawdown)
    return {
        "num_of_trade": len(trade_history),
        "total_return": f"{total_return} %",
        "max_drawdown": f"{max_drawdown} %",
    }
