from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category
from .forms import ProductForm, CategoryForm
from django.contrib import messages
from django.db import models


# View para listar todos os produtos
def product_list(request):
    query = request.GET.get("q", "")
    category_id = request.GET.get("category", None)
    order = request.GET.get("order", "name")

    products = Product.objects.all()

    if query:
        products = products.filter(
            models.Q(name__icontains=query)
            | models.Q(description__icontains=query)
            | models.Q(category__name__icontains=query)
        )

    if category_id:
        products = products.filter(category_id=category_id)

    valid_orders = ["name", "price", "-price", "stock"]
    if order in valid_orders:
        products = products.order_by(order)

    return render(
        request,
        "store/product_list.html",
        {
            "products": products,
            "query": query,
            "categories": Category.objects.all(),
            "selected_category": category_id,
            "order": order,
        },
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
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
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


# View para criar produtos
def category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = CategoryForm()

    return render(request, "store/category_form.html", {"form": form})
