def cart_counter(request):
    cart = request.session.get("cart", [])
    total_items = sum(item["quantity"] for item in cart)
    return {"cart_count": total_items}
