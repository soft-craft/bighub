from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    
    path('<int:id>/<slug:slug>/', views.product_detail,name='product_detail'),
    path('submit_product', views.submit_product,name='submit_product'),
    path('get_best_price/<int:id>', views.get_best_price, name='get_best_price')
]
