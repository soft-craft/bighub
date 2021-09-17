from django.db import reset_queries
from django.shortcuts import redirect, render
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.shortcuts import get_object_or_404
from .forms import MyPasswordChangeForm, UserRegistrationForm, UserEditForm, ProfileEditForm, RetailerForm, SupplierForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import *
from suppliers.models import Supplier

# Create your views here.

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name  = request.POST['last_name']
        username  = request.POST['username']
        email  = request.POST['email']
        password  = request.POST['password']
        confirm_password  = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken. Try a different one!')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered!')
                return redirect('register')
            else:
                user = User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    password=password
                )
                user.save()
                messages.success(request, 'Your account has been created. Login to continue!')
                return redirect('login')
        else:
            messages.error(request, 'Password fields do not match!')
            return redirect('register')
    else:
        return render(request,'account/register.html')
    

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
def post_requirements(request):
    if request.method == 'POST':
        current_user = request.user.username
        buyer = User.objects.get(username=current_user)
        try:
            product_attribute = request.POST['product']
            products = Products.objects.all()
            product = products.filter(Q(product_name__icontains=product_attribute) | Q(description__icontains=product_attribute))
        except Products.DoesNotExist:
            product = None
        quantity_required = request.POST['quantity']
        request_description = request.POST['description']
        for pr in product:
            try:
                supplier_user = User.objects.get(username=pr.supplier.user.username)
                supplier = Supplier.objects.get(user=supplier_user)
            except Supplier.DoesNotExist:
                supplier = None

            primary_leads = Primary_leads(seller=supplier, buyer=buyer, product=pr,
                                        quantity_required=quantity_required,
                                        request_description=request_description)
            primary_leads.save()
        return redirect('home')
    else:
        return render(request, 'account/post_requirements.html')


@login_required
def dashboard(request):
    current_profile = request.user.profile
    try:
        current_supplier = Supplier.objects.get(user=request.user)
    except Supplier.DoesNotExist:
        current_supplier = None

    latest_buyleads = Primary_leads.objects.filter(seller = current_supplier)[:3]
    all_buyleads_count = Primary_leads.objects.filter(seller=current_supplier).count()

    latest_mbox = Message_box.objects.filter(seller = request.user)[:3]
    all_mbox_count = Message_box.objects.filter(seller = request.user).count()

    print(request.get_full_path())
    return render(request,
                'dashboard/dashboard.html',
                {'section': 'dashboard','current_profile': current_profile,
                'current_supplier':current_supplier,'leads':latest_buyleads,'leads_count':all_buyleads_count, 'mboxes':latest_mbox,'mboxes_count':all_mbox_count})


@login_required
def company_profile(request):

    current_profile = request.user.profile
    try:
        current_supplier = Supplier.objects.get(user=request.user)
    except Supplier.DoesNotExist:
        current_supplier = None

    return render(request,
                'dashboard/company_profile.html',
                {'section': 'dashboard','current_profile': current_profile,'current_supplier':current_supplier})

@login_required
def lead_manager(request):

    current_profile = request.user.profile
    try:
        current_supplier = Supplier.objects.get(user=request.user)
    except Supplier.DoesNotExist:
        current_supplier = None

    sent_messages = Lead_messages.objects.filter()

    return render(request,
                'dashboard/lead_manager.html',
                {'section': 'dashboard','current_profile': current_profile,'current_supplier':current_supplier})

@login_required
def manage_products(request):

    current_profile = request.user.profile
    try:
        current_supplier = Supplier.objects.get(user=request.user)
    except Supplier.DoesNotExist:
        current_supplier = None

    products = Products.objects.filter(supplier=current_supplier)

    return render(request,
                'dashboard/manage_products.html',
                {'section': 'dashboard','current_profile': current_profile,
                 'current_supplier':current_supplier,
                 'products': products})


@login_required
def buy_leads(request):

    current_profile = request.user.profile
    try:
        current_supplier = Supplier.objects.get(user=request.user)
    except Supplier.DoesNotExist:
        current_supplier = None

    latest_buyleads = Primary_leads.objects.filter(seller=current_supplier)[:3]

    return render(request,
                'dashboard/buy_leads.html',
                {'section': 'dashboard','current_profile': current_profile,
                 'current_supplier':current_supplier,
                 'latest_buyleads': latest_buyleads})


@login_required
def collect_payments(request):

    current_profile = request.user.profile
    try:
        current_supplier = Supplier.objects.get(user=request.user)
    except Supplier.DoesNotExist:
        current_supplier = None

    return render(request,
                'dashboard/collect_payments.html',
                {'section': 'dashboard','current_profile': current_profile,'current_supplier':current_supplier})

@login_required
def catalog_view(request):

    current_profile = request.user.profile
    try:
        current_supplier = Supplier.objects.get(user=request.user)
    except Supplier.DoesNotExist:
        current_supplier = None

    return render(request,
                'dashboard/catalog_view.html',
                {'section': 'dashboard','current_profile': current_profile,'current_supplier':current_supplier})

@login_required
def photos_docs(request):

    current_profile = request.user.profile
    try:
        current_supplier = Supplier.objects.get(user=request.user)
    except Supplier.DoesNotExist:
        current_supplier = None

    return render(request,
                'dashboard/photos&docs.html',
                {'section': 'dashboard','current_profile': current_profile,'current_supplier':current_supplier})


@login_required
def bills_invoice(request):

    current_profile = request.user.profile
    try:
        current_supplier = Supplier.objects.get(user=request.user)
    except Supplier.DoesNotExist:
        current_supplier = None

    return render(request,
                'dashboard/bill&invoice.html',
                {'section': 'dashboard','current_profile': current_profile,'current_supplier':current_supplier})


@login_required
def buyer_tools(request):

    current_profile = request.user.profile
    try:
        current_supplier = Supplier.objects.get(user=request.user)
    except Supplier.DoesNotExist:
        current_supplier = None

    return render(request,
                'dashboard/buyer_tools.html',
                {'section': 'dashboard','current_profile': current_profile,'current_supplier':current_supplier})


@login_required
def settings(request):

    current_profile = request.user.profile
    try:
        current_supplier = Supplier.objects.get(user=request.user)
    except Supplier.DoesNotExist:
        current_supplier = None

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


@login_required
def change_password(request):
    if request.method == 'POST':
        change_password_form = MyPasswordChangeForm(user=request.user, data=request.POST)
        if change_password_form.is_valid():
            change_password_form.save()
            # This will update the session and we won't be logged out after changing the password
            update_session_auth_hash(request, change_password_form.user)
            messages.success(request, 'Your password has been updated!')
            return redirect('password_change')
        else:
            messages.success(request, 'Something went wrong. Please try again.')
            return redirect('password_change')
    else:
        change_password_form = MyPasswordChangeForm(user=request.user)
    context = {
               'change_password_form':change_password_form,
               }
    return render(request, 'account/password_change_form.html', context)
    


            




