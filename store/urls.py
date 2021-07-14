from django.urls import path
from . import views

urlpatterns = [
    path("", views.store, name="store"),
    path("carrito/", views.cart, name="cart"),
    path("resumen/", views.checkout, name="checkout"),
    path("update_item/", views.updateItem, name="update_item"),
    path("process_order/", views.processOrder, name="process_order"),
    # usuario
    # path("perfil/", views.profile, name="profile"),
    path("registro/", views.signup, name="signup"),
    path("acceso/", views.signin, name="signin"),
    path("signout/", views.signout, name="signout"),
]
