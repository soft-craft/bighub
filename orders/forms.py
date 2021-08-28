from django import forms
from .models import Order, Quotations
PAYMENT_METHOD  = [("Cash On Delivery", "Cash On Delivery"),
    ("Esewa", "Esewa")]
class OrderCreateForm(forms.ModelForm):
    payment = forms.TypedChoiceField(choices=PAYMENT_METHOD)

    class Meta:
        model = Order
        fields = []


class QuotationForm(forms.ModelForm):

    class Meta:
        model = Quotations
        fields = ['name','email','phone_number','mail_address','product_category','product_name','quantity','description']
