from django.urls import path
from .views import execute_trade

urlpatterns = [
    path('execute_trade/', execute_trade, name='execute_trade'),
]