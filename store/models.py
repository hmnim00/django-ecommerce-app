from django.db import models
from django.contrib.auth.models import AbstractUser

# categorias
CATEGORIAS = [
    ("xbox", "Xbox"),
    ("playstation", "Playstation"),
    ("nintendo", "Nintendo"),
    ("otro", "Otro"),
]

# usuario
class User(AbstractUser):
    pass


# modelo cliente
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=256, null=True)
    email = models.EmailField(max_length=128, null=True)

    def __str__(self):
        return self.name


# modelo producto
class Product(models.Model):
    OTRO = "otro"
    name = models.CharField(max_length=512)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    digital = models.BooleanField(default=False, null=True, blank=True)
    # category = models.CharField(max_length=54, null=True, blank=True)
    category = models.CharField(max_length=54, choices=CATEGORIAS, default=OTRO)
    dateAdded = models.DateTimeField(auto_now_add=True)
    image = models.CharField(max_length=512, null=True, blank=True)
    # image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    # imágen por defecto
    # def imageUrl(self):
    #   try:
    #     url = self.image.url
    #   except:
    #     url = '/store/static/img/no-image.png'
    #   return url


# modelo orden
class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True
    )
    dateOrdered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transactionId = models.CharField(max_length=128, null=True)

    def __str__(self):
        return str(self.id)

    # envío
    # si el producto es digital no se requieren los datos de envío (dirección, estado, ...)
    @property
    def shipping(self):
        shipping = False
        orderItems = self.orderitem_set.all()
        for item in orderItems:
            if item.product.digital == False:
                shipping = True
        return shipping

    # total ($) de los productos
    @property
    def getCartTotal(self):
        orderItems = self.orderitem_set.all()
        total = sum(
            [item.getTotal for item in orderItems]
        )  # Realiza la sumatoria de los precios
        return total

    # total (cantidad) de productos
    @property
    def getCartItems(self):
        orderItems = self.orderitem_set.all()
        total = sum(
            [item.quantity for item in orderItems]
        )  # Sumatoria de los productos (cantidad)
        return total


# modelo elementos en orden
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    dateAdded = models.DateTimeField(auto_now_add=True)

    # calcular cantidad total (precio del producto por cantidad del mismo)
    @property
    def getTotal(self):
        total = self.product.price * self.quantity
        return total


# modelo envío
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=256, null=False)
    city = models.CharField(max_length=128, null=False)
    state = models.CharField(max_length=128, null=False)
    zipcode = models.CharField(max_length=16, null=False)
    phone = models.CharField(max_length=16, null=False)
    dateAdded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
