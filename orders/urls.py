from django.urls import path
from . import views
from orders.views import order_create, EsewaRequestView, EsewaVerifyView, req_quotation

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path("esewa-request/", EsewaRequestView.as_view(), name="esewarequest"),
    path("esewa-verify/", EsewaVerifyView.as_view(), name="esewaverify"),
    path("request-quotation/",views.req_quotation, name="request_quotation" )

    
]
