from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib import auth
from django.contrib.auth.models import User, Permission
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.core.mail import send_mail
from .forms import LoginForm, StockForm, ProductForm
from .models import Bill,BillItem, Product, Stock
import json

# admin  => admin, Test123
# demouser => demouser, Testpass@123
# Create your views here.
def index(request):
    return render(request,'smartapp/index.html')


def login(request):
    if(request.method =="POST"):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(request=request,username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                auth.login(request,user)
                print(dir(user))
                if not user.is_active:
                    return render(request,'smartapp/login.html',{'form':form,'msg':"This account is not active."})
                if user.is_superuser:
                    return redirect(to="../admindash",request=request)
                    # return redirect(to='../admin/',request=request)
                if user.is_staff:
                    return redirect(to='../staff/',request=request)
            else:
                return render(request,'smartapp/login.html',{'form':form,'msg':"No user found, Please login with proper credentials or signup"})
        else:
            print("Invalid Login Form")
            return render(request,'smartapp/login.html',{'form':form,'msg':"Invalid Details !"})
    form = LoginForm()
    return render(request,'smartapp/login.html',{'form':form})


def logout(request):
    auth.logout(request)
    return redirect('/')


@login_required
def staff_home(request):
    return render(request,'smartapp/staffhome.html',{'user':request.user})


@login_required
def staff_billing(request):
    bills = Bill.objects.all().order_by("-id")
    # print(dir(bills[0]))
    return render(request,'smartapp/staffbill.html',{'bills':bills})


@login_required
def staff_bill_details(request,billno):
    if request.method=="GET":
        bill = Bill.objects.get(billno=billno)
        bill_items = bill.billitem_set.all()
        print(dir(bill_items[0]))
    else:
        bill_items=None
    return render(request,'smartapp/staffbilldetails.html',{'bill_items':bill_items,'bill':bill})


@login_required
@permission_required('smartapp.add_bill')
@permission_required('smartapp.change_bill')
@permission_required('smartapp.add_billitem')
@permission_required('smartapp.change_billitem')
def staff_bill_add(request):
    if request.method == "GET":
        products = Product.objects.all()
        context = {'products':products,'user':request.user}
        return render(request,'smartapp/staffbilladd.html',context)
    if request.method=="POST":
        print("post request received")
        # print(dir(request))
        print(json.loads(request.body.decode('utf-8'))["products"])
        products = json.loads(request.body.decode('utf-8'))["products"]
        # print(request.user)
        user = User.objects.get(username=request.user)
        with transaction.atomic():
            bill = Bill(total=0)
            bill.cashier = user
            bill.save()
            for p in products:
                product = Product.objects.get(pk=p["product"])
                billitem = BillItem()
                billitem.bill = bill
                billitem.product = product
                billitem.quantity = int(p["quantity"])
                billitem.total = int(p['quantity']) * product.price
                billitem.save()
        return HttpResponse("")
    # return render(request,'smartapp/staffbilladd.html')


@login_required
@permission_required('smartapp.view_stock')
def staff_stocks(request):
    stocks = Stock.objects.all().order_by("-id")
    print(dir(stocks[0]))
    context = {'stocks':stocks,'user':request.user}
    return render(request,'smartapp/staffstock.html',context)


@login_required
@permission_required('smartapp.view_stock',raise_exception=True)
# @permission_required('smartapp.change_stock',raise_exception=True)
def staff_edit_stocks(request,id):
    stock = Stock.objects.get(pk=id)
    form = StockForm(instance=stock)
    context = {'stock':stock,'user':request.user, "form":form}
    if request.method=="POST":
        form = StockForm(request.POST,instance=stock)
        if form.is_valid():
            form.save()
            context = {'stock':stock,'user':request.user, "form":form, "msg":"Stock Updated Successfully"}
            return render(request,'smartapp/staffstockedit.html',context)
        else:
            context = {'stock':stock,'user':request.user, "form":form, "err":"Enter valid data"}
            return render(request,'smartapp/staffstockedit.html',context)
    return render(request,'smartapp/staffstockedit.html',context)
   
@login_required
def staff_products(request):
    products = Product.objects.all().order_by("-id")
    context = {'products':products,'user':request.user}
    return render(request,'smartapp/staffproducts.html',context)

@login_required
def staff_products_add(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            form = ProductForm()
            context = {'user':request.user,'form':form, "msg":"Product Added Successfully"}
            return render(request,'smartapp/staffproductsadd.html',context)
        else:
            context = {'user':request.user,'form':form, "err":"Enter valid details"}
            return render(request,'smartapp/staffproductsadd.html',context)
    else:
        form = ProductForm()
        context = {'user':request.user,'form':form}
        return render(request,'smartapp/staffproductsadd.html',context)

@login_required
def staff_products_edit(request,id):
    if request.method == "POST":
        product = Product.objects.get(pk=id)
        form = ProductForm(request.POST,instance=product)
        if form.is_valid():
            form.save()
            product = Product.objects.get(pk=id)
            form = ProductForm(instance=product)
            context = {'user':request.user,'form':form, 'product':product, "msg":"Product Changed Successfully"}
            return render(request,'smartapp/staffproductsedit.html',context)
        else:
            context = {'user':request.user,'form':form, 'product':product, "err":"Enter valid details"}
            return render(request,'smartapp/staffproductsedit.html',context)
    else:
        product = Product.objects.get(pk=id)
        form = ProductForm(instance=product)
        context = {'user':request.user,'form':form,'product':product}
        return render(request,'smartapp/staffproductsedit.html',context)

##############################################################

def product_details(request,id):
    if request.method == "GET":
        if request.GET['dashboard'] == "1":
            product = Product.objects.get(id=id)
            return JsonResponse({'name':product.name,'price':product.price,'code':product.code, 'stock':product.stock.available_quantity})
    return render(request, 'smartapp/productdetails.html')

###############################################################
######################   Admin    #############################
###############################################################


@login_required
def admin_dash(request):
    return render(request,'smartapp/adminhome.html',{'user':request.user})


@login_required
def admin_list_users(request):
    # print(dir(User.objects.all()[0]))
    staffs = User.objects.filter(is_staff=True, is_superuser=False)
    admins = User.objects.filter(is_superuser=True)
    # others = User.objects.filter(is_superuser=False,is_staff=False)
    context = {
        'staffs':staffs,
        'admins':admins,
        # 'others':others,
        'user':request.user
    }
    return render(request,'smartapp/adminlistusers.html',context)


@login_required
def admin_add_staff_users(request):
    form = UserCreationForm()
    context = {'form':form}
    if request.method=="POST":
        form = UserCreationForm(request.POST)
        stafftype = request.POST["stafftype"]
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]
        print(stafftype)
        if form.is_valid():
            newuser = form.save()
            newuser.is_staff = True
            newuser.first_name = first_name
            newuser.last_name = last_name
            if stafftype == "cashier":
                addbillpermission = Permission.objects.get(codename="add_bill")
                viewbillpermission = Permission.objects.get(codename="view_bill")
                # changebillpermission = Permission.objects.get(codename="change_bill")
                # deletebillpermission = Permission.objects.get(codename="delete_bill")
                addbillitempermission = Permission.objects.get(codename="add_billitem")
                viewbillitempermission = Permission.objects.get(codename="view_billitem")
                # changebillitempermission = Permission.objects.get(codename="change_billitem")
                # deletebillitempermission = Permission.objects.get(codename="delete_billitem")

                viewproductpermission = Permission.objects.get(codename="view_product")

                newuser.user_permissions.add(addbillpermission)
                newuser.user_permissions.add(viewbillpermission)
                # newuser.user_permissions.add(changebillpermission)
                # newuser.user_permissions.add(deletebillpermission)
                newuser.user_permissions.add(addbillitempermission)
                newuser.user_permissions.add(viewbillitempermission)
                # newuser.user_permissions.add(changebillitempermission)
                # newuser.user_permissions.add(deletebillitempermission)
                newuser.user_permissions.add(viewproductpermission)
                newuser.save()
            elif stafftype == "stock":
                viewstockpermission = Permission.objects.get(codename="view_stock")
                changestockpermission = Permission.objects.get(codename="change_stock")
                viewproductpermission = Permission.objects.get(codename="view_product")

                newuser.user_permissions.add(viewstockpermission)
                newuser.user_permissions.add(changestockpermission)
                newuser.user_permissions.add(viewproductpermission)
                newuser.save()
            form = UserCreationForm()
            context = {'form':form,"msg":"Staff added successfully"}
            return render(request,'smartapp/adminaddstaffusers.html',context)
        else:
            context = {'form':form,'err':'Enter Valid Details'}
            return render(request,'smartapp/adminaddstaffusers.html',context)
    return render(request,'smartapp/adminaddstaffusers.html',context)


@login_required
def admin_add_admin_users(request):
    form = UserCreationForm()
    context = {'form':form}
    if request.method=="POST":
        form = UserCreationForm(request.POST)
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]
        if form.is_valid():
            newuser = form.save()
            newuser.is_staff = True
            newuser.is_superuser = True
            newuser.first_name = first_name
            newuser.last_name = last_name
            newuser.save()
            form = UserCreationForm()
            context = {'form':form,"msg":"Staff added successfully"}
            return render(request,'smartapp/adminaddadminusers.html',context)
        else:
            context = {'form':form,'err':'Enter Valid Details'}
            return render(request,'smartapp/adminaddadminusers.html',context)
    return render(request,'smartapp/adminaddadminusers.html',context)


@login_required
def admin_edit_users(request,id):
    user = User.objects.get(pk=id)
    form = UserChangeForm(instance=user)
    iscashier = user.has_perms(( "smartapp.add_bill", "smartapp.view_bill", "smartapp.add_billitem", "smartapp.view_billitem", "smartapp.view_product",))
    isstock = user.has_perms(( "smartapp.view_product", "smartapp.view_stock", "smartapp.change_stock",))
    print("iscashier ",iscashier)
    print("isstock ",isstock)
    context = {'form':form,'user':user,'iscashier':iscashier,'isstock':isstock}
    if request.method=="POST":
        form = UserChangeForm(request.POST,instance=user)
        stafftype = request.POST.get("stafftype",default=None)
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]
        print(stafftype)
        if form.is_valid():
            newuser = form.save()
            newuser.is_staff = True
            newuser.is_active=True
            newuser.first_name = first_name
            newuser.last_name = last_name
            newuser.save()
            if stafftype is not None:
                if stafftype == "admin":
                    newuser.is_superuser=True
                    newuser.save()
                elif stafftype == "cashier":
                    addbillpermission = Permission.objects.get(codename="add_bill")
                    viewbillpermission = Permission.objects.get(codename="view_bill")
                    # changebillpermission = Permission.objects.get(codename="change_bill")
                    # deletebillpermission = Permission.objects.get(codename="delete_bill")
                    addbillitempermission = Permission.objects.get(codename="add_billitem")
                    viewbillitempermission = Permission.objects.get(codename="view_billitem")
                    # changebillitempermission = Permission.objects.get(codename="change_billitem")
                    # deletebillitempermission = Permission.objects.get(codename="delete_billitem")

                    viewproductpermission = Permission.objects.get(codename="view_product")

                    newuser.user_permissions.add(addbillpermission)
                    newuser.user_permissions.add(viewbillpermission)
                    # newuser.user_permissions.add(changebillpermission)
                    # newuser.user_permissions.add(deletebillpermission)
                    newuser.user_permissions.add(addbillitempermission)
                    newuser.user_permissions.add(viewbillitempermission)
                    # newuser.user_permissions.add(changebillitempermission)
                    # newuser.user_permissions.add(deletebillitempermission)
                    newuser.user_permissions.add(viewproductpermission)
                    newuser.is_staff = True
                    newuser.is_active=True
                    newuser.is_superuser = False
                    newuser.save()
                elif stafftype == "stock":
                    viewstockpermission = Permission.objects.get(codename="view_stock")
                    changestockpermission = Permission.objects.get(codename="change_stock")
                    viewproductpermission = Permission.objects.get(codename="view_product")

                    newuser.user_permissions.add(viewstockpermission)
                    newuser.user_permissions.add(changestockpermission)
                    newuser.user_permissions.add(viewproductpermission)
                    newuser.is_staff = True
                    newuser.is_active=True
                    newuser.is_superuser = False
                    newuser.save()
            user = User.objects.get(pk=id)
            iscashier = user.has_perms(( "smartapp.add_bill", "smartapp.view_bill", "smartapp.add_billitem", "smartapp.view_billitem", "smartapp.view_product",))
            isstock = user.has_perms(( "smartapp.view_product", "smartapp.view_stock", "smartapp.change_stock",))
            form = UserChangeForm(instance=user)
            context = {'form':form,"msg":"Staff added successfully",'user':user,'iscashier':iscashier,'isstock':isstock}
            return render(request,'smartapp/admineditusers.html',context)
        else:
            context = {'form':form,'err':'Enter Valid Details','user':user,'iscashier':iscashier,'isstock':isstock}
            return render(request,'smartapp/admineditusers.html',context)
    return render(request,'smartapp/admineditusers.html',context)