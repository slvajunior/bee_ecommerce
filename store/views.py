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


# View add no carrinho
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get("cart", [])  # Corrigido: "cart" ao invés de "card"

    for item in cart:
        if item["product_id"] == product.id:
            item["quantity"] += 1
            item["subtotal"] = float(item["quantity"] * product.price)
            break
    else:
        cart.append(
            {
                "product_id": product.id,
                "name": product.name,
                "price": float(product.price),
                "quantity": 1,
                "subtotal": float(product.price),
            }
        )

    request.session["cart"] = cart
    return redirect("cart_view")  # Alterado para redirecionar ao carrinho


# View do carrinho
def cart_view(request):
    cart = request.session.get("cart", [])
    total = sum(item["quantity"] * item["price"] for item in cart)
    return render(request, "store/cart_view.html", {"cart": cart, "total": total})


# View de remover do carrinho
def remove_from_cart(request, product_id):
    cart = request.session.get("cart", [])

    cart = [item for item in cart if item["product_id"] != product_id]

    request.session["cart"] = cart
    return redirect("cart_view")


# View calcula o total do carrinho
def checkout(request):
    cart = request.session.get("cart", [])

    if not cart:
        messages.error(request, "O carrinho está vazio.")
        return redirect("product_list")

    total = sum(item["subtotal"] for item in cart)

    request.session["cart"] = []
    messages.success(request, "Compra realizada com sucesso.")

    return render(request, "store/checkout.html", {"total": total})


def home(request):
    products = Product.objects.all()
    return render(request, "store/home.html", {"products": products})
