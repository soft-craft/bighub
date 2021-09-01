from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.



STATES = (
    ("Province 1","Province 1"),
    ("Province 2","Province 2"),
    ("Bagmati","Bagmati"),
    ("Gandaki","Gandaki"),
    ("Lumbini","Lumbini"),
    ("Karnali","Karnali"),
    ("Sudur Paschim","Sudur Paschim")
)


class Retailer(models.Model):


    user = models.OneToOneField(User,on_delete=models.CASCADE)

    shop_name = models.CharField(max_length=250, null=False,blank=False)
    proprietor = models.CharField(max_length=50)
    state = models.CharField(max_length=50,choices=STATES)
    city = models.CharField(max_length=20)
    street = models.CharField(max_length=100)
    phone_number = models.PositiveIntegerField()

    verified = models.BooleanField(default=False)
    

    def __str__(self):
        return self.shop_name





