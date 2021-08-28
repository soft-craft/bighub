from django.db import models
from products.models import Products,Category
from retailers.models import Retailer
from django.conf import settings

# Create your models here.

'''
class Cart(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True)
    
    total = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Cart: " + str(self.id)


class CartProduct(models.Model):
    
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()

    def __str__(self):
        return "Cart: " + str(self.cart.id) + " CartProduct: " + str(self.id)

'''

class Order(models.Model):
    #cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(max_length=50, default='')
    retailer = models.ForeignKey(Retailer, on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Products,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        
        return self.price * self.quantity



class Quotations(models.Model):

    name = models.CharField(max_length=50, blank=False,null=False)
    email = models.EmailField()
    phone_number = models.DecimalField(decimal_places=0,max_digits=13)
    mail_address = models.CharField(max_length=200)

    product_category = models.ForeignKey(Category, on_delete=models.CASCADE)

    product_name = models.CharField(max_length=50)
    quantity = models.CharField(max_length = 30)
    description = models.CharField(max_length=200)
    





