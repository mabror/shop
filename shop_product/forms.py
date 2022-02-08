from django import forms
from django.db.models import query
from .models import Product, Order
from django.core.exceptions import ValidationError




class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'city', 'district', 'street', 'house_number']


class AddProduct(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2, 'cols': 21}),
        }
