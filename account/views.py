from django.shortcuts import redirect, render
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm, RetailerForm, SupplierForm
from django.contrib.auth.decorators import login_required
from .models import *
from suppliers.models import Supplier

# Create your views here.

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)

            return render(request, 'account/register_done.html',{'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,'account/register.html',{'user_form': user_form})
    

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Disabled account')
                return redirect('login')
        else:
            messages.error(request, 'Your username and password didn\'t match. Please try again.')
            return redirect('login')
    else:
        return render(request, 'account/login.html')


@login_required
def dashboard(request):
    current_profile = request.user.profile
    current_supplier = Supplier.objects.get(user=request.user)

    latest_buyleads = Primary_leads.objects.filter(seller = current_supplier)[:3]
    all_buyleads_count = Primary_leads.objects.filter(seller=current_supplier).count()

    latest_mbox = Message_box.objects.filter(seller = request.user)[:3]
    all_mbox_count = Message_box.objects.filter(seller = request.user).count()

    print(request.get_full_path())
    return render(request,
                'dashboard/dashboard.html',
                {'section': 'dashboard','current_profile': current_profile,'current_supplier':current_supplier,'leads':latest_buyleads,'leads_count':all_buyleads_count, 'mboxes':latest_mbox,'mboxes_count':all_mbox_count})


@login_required
def company_profile(request):

    current_profile = request.user.profile
    current_supplier = Supplier.objects.get(user=request.user)

    return render(request,
                'dashboard/company_profile.html',
                {'section': 'dashboard','current_profile': current_profile,'current_supplier':current_supplier})

@login_required
def lead_manager(request):

    current_profile = request.user.profile
    current_supplier = Supplier.objects.get(user=request.user)

    sent_messages = Lead_messages.objects.filter()

    return render(request,
                'dashboard/lead_manager.html',
                {'section': 'dashboard','current_profile': current_profile,'current_supplier':current_supplier})

@login_required
def manage_products(request):

    current_profile = request.user.profile
    current_supplier = Supplier.objects.get(user=request.user)

    return render(request,
                'dashboard/manage_products.html',
                {'section': 'dashboard','current_profile': current_profile,'current_supplier':current_supplier})

@login_required
def buy_leads(request):

    current_profile = request.user.profile
    current_supplier = Supplier.objects.get(user=request.user)

    return render(request,
                'dashboard/buy_leads.html',
                {'section': 'dashboard','current_profile': current_profile,'current_supplier':current_supplier})


@login_required
def collect_payments(request):

    current_profile = request.user.profile
    current_supplier = Supplier.objects.get(user=request.user)

    return render(request,
                'dashboard/collect_payments.html',
                {'section': 'dashboard','current_profile': current_profile,'current_supplier':current_supplier})

@login_required
def catalog_view(request):

    current_profile = request.user.profile
    current_supplier = Supplier.objects.get(user=request.user)

    return render(request,
                'dashboard/catalog_view.html',
                {'section': 'dashboard','current_profile': current_profile,'current_supplier':current_supplier})

@login_required
def photos_docs(request):

    current_profile = request.user.profile
    current_supplier = Supplier.objects.get(user=request.user)

    return render(request,
                'dashboard/photos&docs.html',
                {'section': 'dashboard','current_profile': current_profile,'current_supplier':current_supplier})


@login_required
def bills_invoice(request):

    current_profile = request.user.profile
    current_supplier = Supplier.objects.get(user=request.user)

    return render(request,
                'dashboard/bill&invoice.html',
                {'section': 'dashboard','current_profile': current_profile,'current_supplier':current_supplier})


@login_required
def buyer_tools(request):

    current_profile = request.user.profile
    current_supplier = Supplier.objects.get(user=request.user)

    return render(request,
                'dashboard/buyer_tools.html',
                {'section': 'dashboard','current_profile': current_profile,'current_supplier':current_supplier})


@login_required
def settings(request):

    current_profile = request.user.profile
    current_supplier = Supplier.objects.get(user=request.user)

    return render(request,
                'dashboard/settings.html',
                {'section': 'dashboard','current_profile': current_profile,'current_supplier':current_supplier})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                    data=request.POST,
                                    files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})


def register_retailer(request):
    current_user = request.user

    if request.method == 'POST':
        retailer_form = RetailerForm(request.POST)

        if retailer_form.is_valid():
            new_retailer = retailer_form.save(commit=False)
            new_retailer.user = current_user
            new_retailer.save()

            current_user.linked = True
            current_user.save()

            user_profile = Profile.objects.filter(user=current_user).first()
            user_profile.linked = True
            user_profile.save()

            return render(request, 'account/verifying_you.html',{'new_retailer':new_retailer,'current_user':current_user})

    else:
        retailer_form = RetailerForm()

    return render(request,'account/get_verified_retailer.html',{'retailer_form':retailer_form})


def register_supplier(request):
    current_user = request.user

    if request.method == 'POST':
        supplier_form = SupplierForm(request.POST)

        if supplier_form.is_valid():
            new_supplier = supplier_form.save(commit=False)
            new_supplier.user = current_user
            new_supplier.save()

            current_user.linked = True
            current_user.save()

            user_profile = Profile.objects.filter(user=current_user).first()
            user_profile.linked = True
            user_profile.save()

            return render(request, 'account/verifying_you.html',{'new_supplier':new_supplier,'current_user':current_user})

    else:
        supplier_form = SupplierForm()

    return render(request,'account/get_verified_supplier.html',{'supplier_form':supplier_form})



    


            



