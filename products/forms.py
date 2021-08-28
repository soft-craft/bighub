from django import forms
from .models import Products



class SubmitProductForm(forms.ModelForm):

    

    class Meta:
        model = Products
        fields = ['product_name','description','category','image','price','minimum_order_quantity']
        #prepopulated_fields = {'slug': ('product_name',)}