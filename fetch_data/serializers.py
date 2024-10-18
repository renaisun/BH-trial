from rest_framework import serializers
from .models import DailyStockPrice
from datetime import datetime


class DailyStockPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyStockPrice
        fields = ['date', 'open_price', 'high_price', 'low_price', 'close_price', 'volume']

    def create(self, validated_data):
        time_series = validated_data.get('time_series')
        stock_symbol = validated_data.get('stock_symbol')

        dates_from_time_series = [datetime.strptime(date_str, '%Y-%m-%d').date() for date_str in time_series.keys()]
        # 查询数据库中已有的记录
        existing_entries = DailyStockPrice.objects.filter(
            stock_symbol__exact=stock_symbol,
            date__in=dates_from_time_series
        ).values_list('date')
        existing_dates = set([entry[0] for entry in existing_entries])

        # 保存每日的股票数据
        stock_entries = []
        for date_str, stock_data in time_series.items():
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            if date in existing_dates:
                continue
            stock_entry = DailyStockPrice(
                stock_symbol=stock_symbol,  # 从外部传入的 stock_symbol
                date=date,
                open_price=stock_data['1. open'],
                high_price=stock_data['2. high'],
                low_price=stock_data['3. low'],
                close_price=stock_data['4. close'],
                volume=int(stock_data['5. volume']),
            )
            stock_entries.append(stock_entry)
        DailyStockPrice.objects.bulk_create(stock_entries)
        return stock_entries

    def to_internal_value(self, data):
        # 将数据中的 `Time Series (Daily)` 部分提取出来用于解析
        time_series = data.get('Time Series (Daily)', {})
        stock_symbol = data.get('stock_symbol')  # 获取传入的 stock_symbol

        return {
            'time_series': time_series,
            "stock_symbol": stock_symbol
        }
