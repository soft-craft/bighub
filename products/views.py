from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import View, TemplateView, CreateView, FormView, DetailView, ListView
from .models import Products,Category
from suppliers.models import Supplier
from account.models import Primary_leads, Message_box, Lead_messages
from cart.forms import CartAddProductForm
from .forms import SubmitProductForm
from django.utils.text import slugify
from django.http import JsonResponse
import datetime




# Create your views here.

class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_products = Products.objects.all().order_by("-id")
        categories = Category.objects.all().order_by("id")
        context['products'] = all_products
        context['categories'] = categories

        return context

    

def product_detail(request,id,slug):
    product = get_object_or_404(Products,id=id,slug=slug,available=True)

    if request.method == 'POST':

        new_lead = Primary_leads(seller = product.supplier, buyer = request.user, product = product)
        new_lead.save()

        mbox_title = str(product.supplier) + " - " + request.user.first_name + " - " + str(product)

        new_mbox = Message_box(lead = new_lead, title = mbox_title, initiated = datetime.datetime.now(), seller=product.supplier.user, buyer= request.user)
        new_mbox.save()

        first_message = Lead_messages(m_box = new_mbox, content = new_lead.get_message(), sender = request.user, reciever = product.supplier.user, time = datetime.datetime.now() )
        first_message.save()

        return render(request,'dashboard/lead_created.html',{'success':'Success'})

    else:
        return render(request,'products/detail.html',{'product':product})



def submit_product(request):
    current_user = request.user

    if request.method == 'POST':
        submit_product_form = SubmitProductForm(request.POST,request.FILES or None)

        if submit_product_form.is_valid():
            new_product = submit_product_form.save(commit=False)
            new_product.supplier = current_user.supplier
            new_product.slug = slugify(new_product.product_name)
            
            new_product.save()
        
            return redirect('dashboard')

    else:
        submit_product_form = SubmitProductForm()
        
    return render(request, 'products/submit_product.html',{'submit_product_form':submit_product_form})

 
@login_required
def get_best_price(request, id):
    if request.method == 'POST':
        current_user = request.user.username
        buyer = User.objects.get(username=current_user)
        product = Products.objects.get(id=id)
        supplier = product.supplier

        quantity_required = request.POST['quantity']
        request_description = request.POST['description']

        primary_leads = Primary_leads(seller=supplier, buyer=buyer, product=product,
                                    quantity_required=quantity_required,
                                    request_description=request_description)
        primary_leads.save()
        return redirect('home')
    else:
        return render(request, 'product/detail.html')