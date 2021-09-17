from django.db import models
from products.models import Products
from django.contrib.auth.models import User

# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return float(self.quantity * self.product.price)

    price = models.FloatField(default=get_total_price)

    def __str__(self):
        return self.user.username