from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from collections import defaultdict

from .models import Order, Trade

rs = set([1,2,3])

stock_thread_dict = dict()

stock_list_dict = dict()

class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    template_name = 'orders/order_create.html'
    fields = ['type', 'side', 'price', 'quantity', 'stock_code']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/order_list.html'
    ordering =['-timestamp']
    context_object_name='orders'

class OrderUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Order
    fields = ['type', 'side', 'price', 'quantity', 'stock_code']
    template_name = 'orders/order_update.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        order = self.get_object()
        if order.user == self.request.user:
            return True
        else:
            return False

class OrderDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Order
    success_url ='/orders'

    def test_func(self):
        order = self.get_object()
        if order.user == self.request.user:
            return True
        else:
            return False

class TradeListView(LoginRequiredMixin, ListView):
    model = Trade
    template_name = 'orders/trade_list.html'
    ordering =['-timestamp']
    context_object_name='trades'