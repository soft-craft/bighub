from django.db import models
from django.conf import settings


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


class Supplier(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    state = models.CharField(max_length=50,choices=STATES)
    city = models.CharField(max_length=20)
    street = models.CharField(max_length=100)
    phone_number = models.PositiveIntegerField()

    verified = models.BooleanField(default=False)


    def __str__(self):

        return self.name