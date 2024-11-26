from django.db import models
from django.core.files.images import ImageFile
from PIL import Image
import io


# Definição do Modelo de Produto
class Product(models.Model):
    name = models.CharField(max_length=225)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    description = models.TextField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    featured = models.BooleanField(default=False)

    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, null=True, blank=True
    )


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="additional_images"
    )
    image = models.ImageField(upload_to="products/extra_images/")

    def save(self, *args, **kwargs):
        if self.image:
            img = Image.open(self.image)
            img = img.resize((854, 480))
            img_io = io.BytesIO()
            img.save(img_io, format="JPEG")
            img_file = ImageFile(img_io, name=self.image.name)
            self.image = img_file
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Extra image for {self.product.name}"


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
