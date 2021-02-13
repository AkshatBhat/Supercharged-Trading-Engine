from django.urls import path, include

from .views import OrderCreateView, OrderListView, OrderUpdateView, OrderDeleteView, TradeListView

urlpatterns = [
    path('api/', include('orders.api.urls')),
    path('orders/', OrderListView.as_view(), name = 'orders-list'),
    path('orders/new/', OrderCreateView.as_view(), name = 'order-create'),
    path('orders/<int:pk>/update/', OrderUpdateView.as_view(), name = 'order-update'),
    path('orders/<int:pk>/delete/', OrderDeleteView.as_view(), name = 'order-delete'),
    path('trades/', TradeListView.as_view(), name = 'trades-list'),
]