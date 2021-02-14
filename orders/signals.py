from django.db.models.signals import post_save,post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Order,Trade
from .views import stock_thread_dict,stock_list_dict
from . import engine as m_engine
import threading

@receiver(post_save, sender=Order)
def create_order(sender, instance, created, **kwargs):
    # if instance.stock_code not in stock_list_dict.keys():
    #     stock_list_dict[instance.stock_code] = list(Order.objects.all().filter(stock_code=instance.stock_code))
    if created:
        order_list = list(Order.objects.all().filter(stock_code=instance.stock_code))

        engine = m_engine.MatchingEngine()

        if instance.stock_code not in stock_thread_dict.keys():
            t = threading.Thread(target=engine.run,daemon=True)
            t.start()
            stock_thread_dict[instance.stock_code] = t

        curr_thread = stock_thread_dict[instance.stock_code]
        print("Alive",curr_thread.is_alive())

        for order in order_list:
            engine.process(order)

        print(stock_thread_dict)
    print('Order signal called\n')

@receiver(post_delete, sender=Order)
def delete_order(sender, instance, **kwargs):
    print('Order deleted signal called\n')