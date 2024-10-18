from predict_data.views import get_future_stock_price, predict_and_visualize

from django.urls import path, include

urlpatterns = [
    path('predict', get_future_stock_price, name='get-future-stock-price'),
    path('predict_and_visualize', predict_and_visualize, name='predict-and-visualize')
]
