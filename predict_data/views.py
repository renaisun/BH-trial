import pickle

from django.http import JsonResponse
from rest_framework.decorators import api_view
from sklearn.linear_model import LinearRegression
from collections import deque
from fetch_data.models import DailyStockPrice
import plotly.graph_objects as go
from django.shortcuts import render


class ModelRegistry:
    _instance = None
    _model: object = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelRegistry, cls).__new__(cls)
        return cls._instance

    @classmethod
    def load_models(cls):
        """Load all pre-trained models from the models directory"""
        cls._model = LinearRegression()
        with open("models/model.pkl", 'rb') as f:
            cls._model = pickle.load(f)

    @classmethod
    def get_model(cls):
        if cls._model is None:  # Ensure model is loaded
            cls.load_models()
        return cls._model


@api_view(['GET'])
def get_future_stock_price(request):
    stock_symbol = request.GET.get('symbol')
    duration = request.GET.get('duration')

    if stock_symbol is None:
        return JsonResponse({"message": "symbol is required"}, status=400)
    if duration is None:
        return JsonResponse({"message": "duration is required"}, status=400)

    duration = int(duration)
    results = DailyStockPrice.objects.filter(
        stock_symbol=stock_symbol
    ).order_by('-date')[:5].values()
    results = results[::-1]
    if len(results) < 5:
        return JsonResponse({"message": f"not enough history data for {stock_symbol}"}, status=400)

    model = ModelRegistry.get_model()
    future_price = []
    history_price = [float(ent['close_price']) for ent in results]
    dq = deque(history_price)
    for _ in range(duration):
        predicted_value = model.predict([dq])[0]
        future_price.append(predicted_value)
        dq.popleft()
        dq.append(predicted_value)

    return JsonResponse({"message": "success", "future_days_price": future_price})


@api_view(['GET'])
def predict_and_visualize(request):
    stock_symbol = request.GET.get('symbol')
    duration = request.GET.get('duration')

    if stock_symbol is None:
        return JsonResponse({"message": "symbol is required"}, status=400)
    if duration is None:
        return JsonResponse({"message": "duration is required"}, status=400)

    duration = int(duration)
    results = DailyStockPrice.objects.filter(
        stock_symbol=stock_symbol
    ).order_by('-date')[:duration].values()
    if len(results) < duration:
        return JsonResponse({"message": f"not enough history data for {stock_symbol}"}, status=400)

    dq = deque([float(ent['close_price']) for ent in results[:5]])
    model = ModelRegistry.get_model()
    for i in range(5, len(results)):
        predicted = model.predict([dq])[0]
        results[i]['predict'] = predicted
        dq.popleft()
        dq.append(float(results[i]['close_price']))
    x = [ent['date'] for ent in results]
    y_true = [float(ent['close_price']) for ent in results]
    y_pred = [float(ent['predict']) for ent in results if 'predict' in ent]
    fig = go.Figure(data=[
        go.Line(x=x, y=y_true, mode='lines+markers', name='Ground Truth'),
        go.Line(x=x[5:-5], y=y_pred, mode='lines+markers', name='Predict')
    ])

    fig.update_layout(barmode='group', title=f"Trend price over the last {duration} days", xaxis_title="Date",
                      yaxis_title="Values")

    chart_html = fig.to_html(full_html=False)

    return render(request, 'charts.html', {'chart_html': chart_html})
