# myapp/urls.py

from django.urls import path
from .views import fetch_and_store_user_data
urlpatterns = [
    path('fetch-data', fetch_and_store_user_data, name='fetch-data'),
]
