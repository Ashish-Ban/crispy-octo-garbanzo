from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.core.mail import send_mail
from .forms import LoginForm, StockForm
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
                    return redirect(to='../admin/',request=request)
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
    bills = Bill.objects.all()
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
    stocks = Stock.objects.all()
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
   

def product_details(request,id):
    if request.method == "GET":
        if request.GET['dashboard'] == "1":
            product = Product.objects.get(id=id)
            return JsonResponse({'name':product.name,'price':product.price,'code':product.code, 'stock':product.stock.available_quantity})
    return render(request, 'smartapp/productdetails.html')