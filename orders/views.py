from django.shortcuts import render
from cart.cart import Cart
from .models import OrderItem, Order
from .forms import OrderCreateForm,QuotationForm
from django.conf import settings
from retailers.models import Retailer
from django.views.generic import View
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse

from django.http import HttpResponseRedirect
import requests




class EsewaRequestView(View):
    def get(self, request, *args, **kwargs):
        o_id = request.GET.get("o_id")
        order = Order.objects.get(id=o_id)
        total_cost = order.get_total_cost()
        
        context = {
            "order": order,"total_cost":total_cost
        }
        return render(request, "orders/esewarequest.html", context)


class EsewaVerifyView(View):
    def get(self, request, *args, **kwargs):
        import xml.etree.ElementTree as ET
        oid = request.GET.get("oid")
        amt = request.GET.get("amt")
        refId = request.GET.get("refId")

        url = "https://uat.esewa.com.np/epay/transrec"
        d = {
            'amt': amt,
            'scd': 'epay_payment',
            'rid': refId,
            'pid': oid,
        }
        resp = requests.post(url, d)
        root = ET.fromstring(resp.content)
        status = root[0].text.strip()

        order_id = oid.split("_")[1]
        order_obj = Order.objects.get(id=order_id)
        if status == "Success":
            order_obj.paid = True
            order_obj.save()
            return redirect("/")
        else:

            return redirect("/esewa-request/?o_id="+order_id)


def order_create(request):
    cart = Cart(request)
    user = request.user
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            order.first_name=user.first_name
            order.user = user
            

            user_retailer = Retailer.objects.filter(user=user).first()
            order.retailer = user_retailer
            pm = form.cleaned_data.get("payment")
           
                                
            
            order.save()
            
            

            print(user)
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # clear the cart
            cart.clear()

            if pm == "Esewa":
                return redirect(reverse("orders:esewarequest") + "?o_id=" + str(order.id))
            
      
           
            
            return render(request,
                          'orders/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm()
        
    return render(request,
                  'orders/create.html',
                  {'cart': cart, 'form': form})



def req_quotation(request):

    if request.method == 'POST':
        quotation_form = QuotationForm(request.POST)

        if quotation_form.is_valid():
            new_quotation = quotation_form.save(commit=False)
            
            new_quotation.save()

            

            

            return render(request, 'shop/orders/quotation_submitted',{'new_quotation':new_quotation})

    else:
        quotation_form = QuotationForm()

    return render(request,'orders/submit_quotation.html',{'quotation_form':quotation_form})

