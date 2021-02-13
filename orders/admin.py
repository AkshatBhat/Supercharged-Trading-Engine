from django.contrib import admin
from .models import Order, Trade

admin.site.register(Order)
admin.site.register(Trade)