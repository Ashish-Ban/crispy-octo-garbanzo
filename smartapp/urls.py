from django.contrib import admin
from django.urls import path , include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('admindash/',views.admin_dash,name="dashboard"),
    path('admindash/products/',views.admin_products,name="dashboard_products"),
    path('admindash/products/<int:id>/',views.admin_products_edit,name="dashboard_products_edit"),
    path('admindash/products/create/',views.admin_products_add,name="admin_products_add"),
    path('admindash/stocks/',views.admin_stocks,name="dashboard_stocks"),
    path('admindash/stocks/<int:id>/',views.admin_edit_stocks,name="dashboard_edit_stocks"),
    path('admindash/users/',views.admin_list_users,name="dashboard_list_users"),
    path('admindash/users/<int:id>/',views.admin_edit_users,name="dashboard_edit_users"),
    path('admindash/users/createstaff/',views.admin_add_staff_users,name="dashboard_add_staff_users"),
    path('admindash/users/createadmin/',views.admin_add_admin_users,name="dashboard_add_admin_users"),
    path('admin/', admin.site.urls),
    path('login/',views.login,name="login"),
    path('logout/',views.logout,name="logout"),
    path('staff/',views.staff_home,name="staff_home"),
    path('staff/bills/',views.staff_billing,name="staff_billing"),
    path('staff/bills/<uuid:billno>/',views.staff_bill_details,name="staff_bill_details"),
    path('staff/bills/create/',views.staff_bill_add,name="staff_bill_add"),
    path('staff/products/',views.staff_products,name="staff_products"),
    path('staff/products/<int:id>/',views.staff_products_edit,name="staff_products_edit"),
    path('staff/products/create/',views.staff_products_add,name="staff_products_add"),
    path('staff/stocks/',views.staff_stocks,name="staff_stocks"),
    path('staff/stocks/<int:id>/',views.staff_edit_stocks,name="staff_edit_stocks"),
    path('products/<int:id>/',views.product_details,name="product_details"),
    # path('auth/',include('django.contrib.auth.urls')),
    # path("auth/login/",auth_views.LoginView.as_view(template_name="smartapp/login.html")),
]