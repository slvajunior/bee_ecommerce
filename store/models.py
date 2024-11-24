from django.db import models


# Definição do Modelo de Produto
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="products/images/", blank=True, null=True)
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"


class Order(models.Model):
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"Order {self.id} - {self.status}"

    def calculate_total_amount(self):
        total = sum(
            item.product.price * item.quantity for item in self.orderitem_set.all()
        )

        self.total_amount = total
        self.save()
        return total


class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField(max_length=255)

    def __str__(self):
        return self.name


class OrderItem(models.Model):
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
