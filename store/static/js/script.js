let updateBtns = document.querySelectorAll(".carrito-act");

updateBtns.forEach((boton) =>
  boton.addEventListener("click", function () {
    let productId = this.dataset.product;
    let action = this.dataset.action;

    // console.log("usuario: ", user);

    user === "AnonymousUser"
      ? addCookie(productId, action)
      : updateUserOrder(productId, action);
  })
);

// usuarios no loegueados
const addCookie = (productId, action) => {
  // console.log("No está logueado");

  // agregar cantidad de un producto
  if (action == "add") {
    cart[productId] == undefined
      ? (cart[productId] = { quantity: 1 })
      : (cart[productId]["quantity"] += 1);
  }

  // quitar cantidad de un producto
  if (action == "remove") {
    cart[productId]["quantity"] -= 1;

    if (cart[productId]["quantity"] <= 0) {
      // console.log("Remove item");
      delete cart[productId];
    }
  }

  // console.log("CART: ", cart);
  document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/";
  location.reload();
};

//
const updateUserOrder = (productId, action) => {
  let url = "/update_item/";

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ productId, action }),
  })
    .then((res) => {
      return res.json();
    })
    .then((data) => {
      // console.log(data);
      location.reload();
    });
};
