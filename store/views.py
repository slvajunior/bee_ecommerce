from django.shortcuts import render, redirect
from .models import Product
from .forms import ProductForm

# View para listar todos os produtos
def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

# View para criar um novo produto
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()

    return render(request, 'store/product_form.html', {'form': form})
