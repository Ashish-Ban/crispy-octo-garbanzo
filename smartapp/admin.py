from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django.db import models
from .models import BillItem, Product, Stock, Bill

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','price','code','email')
    list_display_links = ('name','price','code','email')
    readonly_field = ('created_at','updated_at')

class StockAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Stock._meta.get_fields()]
    list_display_links = [field.name for field in Stock._meta.get_fields()]
    readonly_field = ('created_at','updated_at')

class BillItemInline(admin.TabularInline):
    model= BillItem
    readonly_fields=('total','created_at','updated_at')

class BillAdmin(admin.ModelAdmin):
    list_display = ('billno','cashier','get_products','total')
    list_display_links = ('billno','cashier','get_products','total')
    inlines = (BillItemInline,)
    readonly_fields = ('created_at','updated_at')

    def get_products(self, obj):
        return "\n".join([p.name for p in obj.products.all()])


# Register your models here.
admin.site.register(Product,ProductAdmin)
admin.site.register(Stock,StockAdmin)
admin.site.register(Bill,BillAdmin)

admin.site.site_header = "SMART"
admin.site.index_title = "SMART Admin Panel"
admin.site.site_title = "SMART Admin"