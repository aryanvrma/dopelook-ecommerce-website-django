from django.urls import path
from . import views

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('returns/', views.refund, name='refunds'),
    path('order_complete/', views.order_complete, name='order_complete'),
]
