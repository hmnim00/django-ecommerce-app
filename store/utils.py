import json
from .models import *


def cookieCart(request):
    # generar nuevo token para usuario sin autenticación
    try:
        cart = json.loads(request.COOKIES["cart"])
    except:
        cart = {}

    items = []
    order = {"getCartTotal": 0, "getCartItems": 0, "shipping": False}
    cartItems = order["getCartItems"]

    # usuario no autenticado
    for i in cart:
        try:
            cartItems += cart[i]["quantity"]

            product = Product.objects.get(id=i)
            total = product.price * cart[i]["quantity"]
            # total ($) y cantidad
            order["getCartTotal"] += total
            order["getCartItems"] += cart[i]["quantity"]
            # loop productos
            item = {
                "product": {
                    "id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "imageUrl": product.imageUrl,
                    "digital": product.digital,
                },
                "quantity": cart[i]["quantity"],
                "getTotal": total,
            }

            items.append(item)

            if product.digital == False:
                order["shipping"] = True
        except:
            pass

    return {"cartItems": cartItems, "order": order, "items": items}


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.getCartItems
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData["cartItems"]
        order = cookieData["order"]
        items = cookieData["items"]

    return {"cartItems": cartItems, "order": order, "items": items}


def guestOrder(request, data):
    print("User not logged")

    print("cookies: ", request.COOKIES)

    name = data["form"]["name"]
    email = data["form"]["email"]

    cookieData = cookieCart(request)
    items = cookieData["items"]

    customer, created = Customer.objects.get_or_create(email=email)
    customer.name = name
    customer.save()

    order = Order.objects.create(customer=customer, complete=False)

    for item in items:
        product = Product.objects.get(id=item["product"]["id"])
        orderItem = OrderItem.objects.create(
            product=product, order=order, quantity=item["quantity"]
        )
    return customer, order
