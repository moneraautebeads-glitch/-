from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # السطر ده هو اللي هيحل المشكلة:
    path('order/<int:pk>/', views.orders, name='create_order'), 
    path('track/', views.track_order, name='track'),
]
