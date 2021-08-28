from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    
    path('<int:id>/<slug:slug>/', views.product_detail,name='product_detail'),
    path('submit_product', views.submit_product,name='submit_product')

]
