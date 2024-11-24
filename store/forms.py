from django import forms
from .models import Product

# Definindo o Formulário de Produto
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock']
