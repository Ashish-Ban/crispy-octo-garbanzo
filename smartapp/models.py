from functools import reduce, total_ordering
from django.db import models
from django.db.models.signals import m2m_changed, post_save, pre_delete
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.dispatch import receiver
import uuid

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100,help_text="Name of the product",blank=False)
    price = models.DecimalField(max_digits=8,decimal_places=2, help_text="Price of product",blank=False)
    code = models.CharField(max_length=30,help_text="Item code",blank=False)
    email = models.EmailField(default="admin@smart.com")

    def __str__(self):
        return self.name

class Stock(models.Model):
    product = models.OneToOneField(Product,on_delete=models.CASCADE,help_text="Product for which the stock is to be entered")
    total_quantity = models.DecimalField(max_digits=8,decimal_places=2,help_text="Total Quantity or capacity for the product",blank=False)
    available_quantity = models.DecimalField(max_digits=8,decimal_places=2,help_text="Available Quantity for the selected product",blank=False)

    def __str__(self):
        return '%d' % self.available_quantity

class Bill(models.Model):
    cashier = models.ForeignKey(User,null=True, on_delete=models.SET_NULL)
    billno = models.UUIDField(default=uuid.uuid4, editable=False)
    products  = models.ManyToManyField(Product, through="smartapp.BillItem")
    total = models.DecimalField(max_digits=8,decimal_places=2,help_text="Total Price of the order",blank=False)

    def __str__(self):
        return '%d' % self.billno

class BillItem(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=8,decimal_places=2,help_text="Product Ordered Quantity",blank=False)
    total = models.DecimalField(max_digits=8,decimal_places=2,help_text="Total Price (Ordered Quantity * Product Price)",blank=False, editable=False)

    def save(self, *args, **kwargs):
        self.total = self.product.price * self.quantity
        super(BillItem, self).save(*args, **kwargs) # Call the "real" save() method.


@receiver(post_save,sender=Product)
def create_stock_entry(sender,instance, **kwargs):
    print("Creating stock entry")
    stock = Stock.objects.filter(product=instance.id)
    if(not len(stock)):
        Stock.objects.create(product=instance,total_quantity=0,available_quantity=0)
        print("Stock Added")
    print("Create stock entry finished")

@receiver(post_save,sender=BillItem)
def calculate_grandTotal(sender,instance, created, **kwargs):
    print("Calculating GrandTotal from billitem post_save")
    bill  = instance.bill
    grandTotal = reduce(lambda x,y:x+y, [float(x.total) for x in bill.billitem_set.all()])
    print("Calculated GrantTotal = {}".format(grandTotal))
    print("Bill.total = {}".format(bill.total))
    if(bill.total!=grandTotal):
        bill.total = grandTotal
        bill.save()
    print("Bill.total updated")
    stock = Stock.objects.filter(product=instance.product.id)
    if(len(stock)):
        stock = stock[0]
        print("Stock Found")
        # print(dir(stock))
        if stock.available_quantity - instance.quantity == 10 :
            send_mail('Product Purchase',"{} is out of stock. We require a delivery of 100 units as soon as possible \n\nThank You, \nSmart store".format(instance.product.name),from_email="banashish5@gmail.com",recipient_list=[instance.product.email])
            stock.available_quantity -=instance.quantity
            stock.save()
        elif stock.available_quantity - instance.quantity > 0 :
            stock.available_quantity -=instance.quantity
            stock.save()

@receiver(pre_delete,sender=BillItem)
def reduce_grandTotal(sender,instance, **kwargs):
    print("Reducing GrandTotal from billitem pre_delete")
    bill  = instance.bill
    grandTotal = bill.total - instance.total
    print("Bill.total = {}".format(bill.total))
    print("New GrandTotal = {}".format(grandTotal))
    if(grandTotal>=0):
        bill.total = grandTotal
        bill.save()
    print("Bill.total updated")