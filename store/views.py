from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .utils import *
from .models import *
import datetime

# página principal
def store(request):
    data = cartData(request)
    cartItems = data["cartItems"]

    products = Product.objects.all()
    paginator = Paginator(products, 15)

    if request.GET.get("page") != None:

        try:
            products = paginator.page(request.GET.get("page"))
        except:
            products = paginator.page(1)

    else:
        products = paginator.page(1)

    context = {"products": products, "cartItems": cartItems, "shipping": False}

    return render(request, "store/index.html", context)


# carrito
def cart(request):
    data = cartData(request)
    cartItems = data["cartItems"]
    order = data["order"]
    items = data["items"]

    context = {"items": items, "order": order, "cartItems": cartItems}

    return render(request, "store/cart.html", context)


# cuenta
def checkout(request):
    data = cartData(request)
    cartItems = data["cartItems"]
    order = data["order"]
    items = data["items"]

    context = {"items": items, "order": order, "cartItems": cartItems}

    if len(items) > 0:
        return render(request, "store/checkout.html", context)
    else:
        return HttpResponseRedirect(reverse("store"))


# actualizar elementos en el carrito
def updateItem(request):
    data = json.loads(request.body)
    productId = data["productId"]
    action = data["action"]

    print("Action: ", action)
    print("Product id: ", productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    # función agregar o quitar elementos
    if action == "add":
        orderItem.quantity = orderItem.quantity + 1
    elif action == "remove":
        orderItem.quantity = orderItem.quantity - 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("Product added", safe=False)


# procesar orden
def processOrder(request):
    transactionId = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)

    total = float(data["form"]["total"])
    order.transactionId = transactionId

    # validar precio
    if total == order.getCartTotal:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data["shipping"]["address"],
            city=data["shipping"]["city"],
            state=data["shipping"]["state"],
            zipcode=data["shipping"]["zipcode"],
            phone=data["shipping"]["phone"],
        )

    return JsonResponse("Payment completed", safe=False)


# nuevo registro
def signup(request):
    if request.method == "POST":

        name = request.POST["name"]
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        # validar campos vacíos
        if not name or not username or not email or not password:
            return render(request, "store/signup.html", {"error": "Hay campos vacíos"})

        # verificar lognitud de contraseña
        if len(password) < 5:
            return render(
                request,
                "store/signup.html",
                {"error": "La contraseña debe ser de al menos 5 caracteres"},
            )

        # verificar contraseña
        if password != confirmation:
            return render(
                request,
                "store/signup.html",
                {"error": "Las contraseñas deben coincidir"},
            )

        print(name, username, email)

        # guardar registro
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            customer = Customer.objects.create(user=user, name=name, email=email)
            customer.save()
        except:
            return render(
                request,
                "store/signup.html",
                {"error": "El nombre de usuario ya está registrado"},
            )

        login(request, user)
        return HttpResponseRedirect(reverse("store"))
    else:
        return render(request, "store/signup.html")


# acceso
def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        # verificar campos
        if not username or not password:
            return render(request, "store/signin.html", {"error": "Hay campos vacíos"})

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("store"))

        else:
            return render(
                request,
                "store/signin.html",
                {"error": "Nombre de usuario o contraseña no válidos"},
            )
    else:
        return render(request, "store/signin.html")


# salir
def signout(request):
    logout(request)
    return HttpResponseRedirect(reverse("store"))


# perfil}
# @login_required
# def profile(request):
#     context = {}
#     return render(request, "store/profile.html", context)
