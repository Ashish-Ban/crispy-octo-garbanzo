from django.contrib import admin
from django.urls import path , include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('',views.index),
    path('admin/', admin.site.urls),
    path('login/',views.login,name="login"),
    path('staff/',views.staff_home,name="staff_home"),
    path('staff/bills/',views.staff_billing,name="staff_billing"),
    path('staff/bills/<uuid:billno>/',views.staff_bill_details,name="staff_bill_details"),
    path('staff/bills/create/',views.staff_bill_add,name="staff_bill_add"),
    path('products/<int:id>/',views.product_details,name="product_details"),
    # path('auth/',include('django.contrib.auth.urls')),
    # path("auth/login/",auth_views.LoginView.as_view(template_name="smartapp/login.html")),
]