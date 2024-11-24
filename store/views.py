from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import ProductForm
from django.contrib import messages


# View para listar todos os produtos
def product_list(request):
    query = request.GET.get("q", "")
    products = (
        Product.objects.filter(name__icontains=query)
        if query
        else Product.objects.all()
    )
    return render(
        request,
        "store/product_list.html",
        {"products": products, "query": query},
    )


# View para criar um novo produto
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Produto criado com sucesso!")
            return redirect("product_list")
    else:
        form = ProductForm()

    return render(request, "store/product_form.html", {"form": form})


# View para exibir detalhes do produto
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, "store/product_detail.html", {"product": product})


# View para editar produto
def product_edit(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Produto atualizado com sucesso!")
            return redirect("product_list")
    else:
        form = ProductForm(instance=product)

    return render(request, "store/product_form.html", {"form": form})


# View para excluir produto
def product_delete(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == "POST":
        product.delete()
        messages.success(request, "Produto excluído com sucesso!")
        return redirect("product_list")
    return render(
        request,
        "store/product_confirm_delete.html",
        {"product": product},
    )
