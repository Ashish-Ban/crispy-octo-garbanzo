from django import forms
from django.db.models import fields
from django.forms import widgets
from .models import Bill, Product, Stock, BillItem

class LoginForm(forms.Form):
    username = forms.CharField(max_length=255,widget=forms.TextInput(attrs={'class':'form-control mb-3'}))
    password = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={'class':'form-control mb-3'}))

    def clean(self):
        cleandata = self.cleaned_data
        if len(cleandata.get('username')) <5:
            self.add_error('username',"Username should atleast contain 5 letters")
        return super().clean()

class StockForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(StockForm,self).__init__(*args,**kwargs)
        
    def clean(self):
        return super().clean()

    class Meta:
        model = Stock
        fields = "__all__"
        exclude = ('created_at','updated_at',)

class ProductForm(forms.ModelForm):
    def __init__(self, *args,**kwargs):
        super(ProductForm,self).__init__(*args,**kwargs)
    
    def clean(self):
        return super().clean()
    
    class Meta:
        model = Product
        fields = "__all__"
        exclude = ('created_at','updated_at',)


class BillItemForm(forms.ModelForm):
    def __init__(self, *args,**kwargs):
        super(BillItemForm,self).__init__(*args,**kwargs)
    
    def clean(self):
        return super().clean()
    
    class Meta:
        model = BillItem
        fields = "__all__"
        exclude = ('created_at','updated_at',)
