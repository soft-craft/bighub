from django import forms
from django.contrib.auth.models import User
from .models import Profile
from retailers.models import Retailer
from suppliers.models import Supplier
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import password_validation


class LoginForm(forms.Form):
    
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control shadow-none', 'id':'floatingName', 'placeholder':'name@example.com'}),
            'last_name': forms.TextInput(attrs={'class':'form-control shadow-none', 'id':'floatingName', 'placeholder':'name@example.com'}),
            'email': forms.TextInput(attrs={'class':'form-control shadow-none', 'id':'floatingName', 'placeholder':'name@example.com'})
        }
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
        }


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('account_type',)
        widgets = {
            'account_type': forms.Select(attrs={'class':'form-control shadow-none', 'id':'floatingName', 'placeholder':'name@example.com'})
        }
        labels = {
            'account_type': 'Account Type'
        }


class RetailerForm(forms.ModelForm):

    class Meta:
        model = Retailer
        fields = ('shop_name','proprietor','state','city','street','phone_number')
        widgets = {
            'shop_name': forms.TextInput(attrs={'class':'form-control shadow-none', 'id':'floatingName', 'placeholder':'name@example.com'}),
            'proprietor': forms.TextInput(attrs={'class':'form-control shadow-none', 'id':'floatingName', 'placeholder':'name@example.com'}),
            'state': forms.Select(attrs={'class':'form-control shadow-none', 'id':'floatingName', 'placeholder':'name@example.com'}),
            'city': forms.TextInput(attrs={'class':'form-control shadow-none', 'id':'floatingName', 'placeholder':'name@example.com'}),
            'street': forms.TextInput(attrs={'class':'form-control shadow-none', 'id':'floatingName', 'placeholder':'name@example.com'}),
            'phone_number': forms.TextInput(attrs={'class':'form-control shadow-none', 'id':'floatingName', 'placeholder':'name@example.com'}),
        }
        labels = {
            'shop_name': 'Shop Name',
            'proprietor': 'Proprietor',
            'state': 'State',
            'city': 'City',
            'street': 'Street',
            'phone_number': 'Phone Number'
        }


class SupplierForm(forms.ModelForm):

    class Meta:
        model = Supplier
        fields = ('name','state','city','street','phone_number')
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control shadow-none', 'id':'floatingName', 'placeholder':'name@example.com'}),
            'state': forms.Select(attrs={'class':'form-control shadow-none', 'id':'floatingName', 'placeholder':'name@example.com'}),
            'city': forms.TextInput(attrs={'class':'form-control shadow-none', 'id':'floatingName', 'placeholder':'name@example.com'}),
            'street': forms.TextInput(attrs={'class':'form-control shadow-none', 'id':'floatingName', 'placeholder':'name@example.com'}),
            'phone_number': forms.TextInput(attrs={'class':'form-control shadow-none', 'id':'floatingName', 'placeholder':'name@example.com'}),
        }
        labels = {
            'name': 'Name',
            'state': 'State',
            'city': 'City',
            'street': 'Street',
            'phone_number': 'Phone Number'
        }


class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
                    strip=False,
                    widget=forms.PasswordInput(attrs={'class':'form-control shadow-none', 'id':'floatingName', 'placeholder':'name@example.com'}),
                    label='Old Password'
                )
    new_password1 = forms.CharField(
                    strip=False,
                    widget=forms.PasswordInput(attrs={'class':'form-control shadow-none', 'id':'floatingName', 'placeholder':'name@example.com'}),
                    help_text=password_validation.password_validators_help_text_html(),
                    label='New Password'
                )
    new_password2 = forms.CharField(
                    strip=False,
                    widget=forms.PasswordInput(attrs={'class':'form-control shadow-none', 'id':'floatingName', 'placeholder':'name@example.com'}),
                    label='Confirm New Password'
                )