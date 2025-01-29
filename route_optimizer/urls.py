from django.urls import path
from .views import route_optimization_api

urlpatterns = [
    path('optimize/', route_optimization_api, name='route_optimization'),
]
