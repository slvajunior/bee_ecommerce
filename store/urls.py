from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("list/", views.product_list, name="product_list"),
    path("create/", views.product_create, name="product_create"),
    path("<int:pk>/", views.product_detail, name="product_detail"),
    path("<int:id>/edit/", views.product_edit, name="product_edit"),
    path("<int:id>/delete/", views.product_delete, name="product_delete"),
    path("add_to_cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.cart_view, name="cart_view"),
    path("checkout/", views.checkout, name="checkout"),  # Define a URL para 'checkout'
    path(
        "remove_from_cart/<int:product_id>/",
        views.remove_from_cart,
        name="remove_from_cart",
    ),
]
