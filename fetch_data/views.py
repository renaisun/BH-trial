# Create your views here.
# myapp/views.py
import json
import os
from datetime import datetime
from http.client import responses

import requests
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import DailyStockPriceSerializer

# URL of external API
EXTERNAL_API_URL = "https://www.alphavantage.co/query"


@api_view(['GET'])
def fetch_and_store_user_data(request):
    stock_symbol = request.GET.get("symbol")
    if stock_symbol is None:
        return JsonResponse({"message": "symbol is required"}, status=400)

    # Make a request to the external API
    request_param = {
        "function": "TIME_SERIES_DAILY",
        "symbol": stock_symbol,
        "apikey": os.getenv("API_KEY"),
        "outputsize": "full"
    }

    try:
        response = requests.get("https://httpbin.org/status/200", params=request_param)
        # for Demo purpose, we get the "response" from file
        # response = requests.get(EXTERNAL_API_URL, params=request_param)
        f = open("demo_data.json", "r")
        data = json.load(f)
        f.close()
        if response.status_code == 200:
            # data = response.json()
            data["stock_symbol"] = stock_symbol
            serializer = DailyStockPriceSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({"message": "Data successfully saved!", "fetched_data": data})
            else:
                return JsonResponse({"error": "Failed to save data", "errors": serializer.errors}, status=400)
        else:
            return JsonResponse({"error": "Failed to fetch data from external API", "status_code": response.status_code,
                             "response": response}, status=400)
    except Exception as e:
        print(f"Unexpected error while processing {stock_symbol}: {str(e)}")
        return JsonResponse({
            "error": "An unexpected error occurred",
            "details": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
