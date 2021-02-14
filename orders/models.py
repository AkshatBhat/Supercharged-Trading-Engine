from django.utils import timezone
from django.db import models
from django.core.validators import MinValueValidator, MinLengthValidator
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse

TYPE_CHOICES = (('M', 'Market'), ('L', 'Limit'),)
SIDE_CHOICES = (('B', 'Buy'), ('S', 'Sell'),)

class Order(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    side = models.CharField(max_length=1, choices=SIDE_CHOICES)
    price = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    stock_code = models.CharField(max_length=6, validators=[MinLengthValidator(6)])
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user}-{self.timestamp}'

    def get_absolute_url(self):
        return reverse('orders-list')

class Trade(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer_user')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_user')
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    timestamp = models.DateTimeField(default=timezone.now)
    price = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    stock_code = models.CharField(max_length=6, validators=[MinLengthValidator(6)])

    def save(self, *args, **kwargs):
        if self.buyer != self.seller:
            super(Trade, self).save(*args, **kwargs)
        else:
            raise ValidationError('Buyer and Seller cannot be same')

    def __str__(self):
        return f'Buyer: {self.buyer}, Seller: {self.seller}'