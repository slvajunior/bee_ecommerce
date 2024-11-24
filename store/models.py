from django.db import models

# Definição do Modelo de Produto
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=100)  # Nome da categoria
    description = models.TextField()         # Descrição da categoria

    def __str__(self):
        return self.name  # Retorna o nome da categoria

class Order(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)  # Relacionamento com o cliente
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)  # Valor total do pedido
    status = models.CharField(max_length=50)  # Status do pedido (ex: 'em andamento', 'enviado')

    def __str__(self):
        return f'Order {self.id} - {self.status}'
        
class Customer(models.Model):
    name = models.CharField(max_length=100)  # Nome do cliente
    email = models.EmailField()              # Email do cliente
    address = models.TextField()             # Endereço do cliente

    def __str__(self):
        return self.name  # Retorna o nome do cliente

