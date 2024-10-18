from django.urls import path

from backtest.views import get_back_rest_result
urlpatterns = [
    path('backtest', get_back_rest_result, name='start-back-test'),
]
