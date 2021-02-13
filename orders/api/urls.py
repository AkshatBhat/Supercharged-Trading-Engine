from django.urls import path

from rest_framework.authtoken import views

from .views import OrderAPIView, OrderDetailAPIView, TradeAPIView, TradeDetailAPIView, signup

urlpatterns = [
    path('signup/', signup),
    path('token/', views.obtain_auth_token),
    path('orders/', OrderAPIView.as_view()),
    path('orders/<int:pk>/', OrderDetailAPIView.as_view()),
    path('trades/', TradeAPIView.as_view()),
    path('trades/<int:pk>/', TradeDetailAPIView.as_view()),
]