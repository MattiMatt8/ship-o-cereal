const CART_URL = "/cart/";
const cartTotalElement = document.getElementById("cart_total");
let cartTotal = Number(cartTotalElement.innerText);

// Function getCookie from: https://docs.djangoproject.com/en/3.0/ref/csrf/#ajax
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const CSRF_TOKEN = getCookie("csrftoken");

function updateCart(id, quantity, callback = undefined, in_cart = false) {
  axios
    .post(
      CART_URL + id + "/",
      { quantity: quantity, in_cart: in_cart },
      { headers: { "X-CSRFToken": CSRF_TOKEN } }
    )
    .then((response) => {
      cartUpdateTotal(quantity, response.data.old_quantity);
      if (callback) {
        callback();
      }
    })
    .catch((error) => {
      console.log(error);
      if (callback) {
        callback(error);
      }
    });
}

function deleteFromCart(id, callback = undefined, in_cart = false) {
  axios
    .post(
      CART_URL + id + "/delete/",
      { in_cart: in_cart },
      { headers: { "X-CSRFToken": CSRF_TOKEN } }
    )
    .then((response) => {
      cartDeleteFromTotal(response.data.quantity);
      if (callback) {
        callback();
      }
    })
    .catch((error) => {
      console.log(error);
      if (callback) {
        callback(error);
      }
    });
}

function cartUpdateTotal(quantity, oldQuantity) {
  cartTotal += quantity - Number(oldQuantity);
  cartTotalElement.innerText = cartTotal;
}

function cartDeleteFromTotal(quantity = 1) {
  cartTotal -= quantity;
  cartTotalElement.innerText = cartTotal;
}


// Searchbar

const searchInput = document.getElementById("search-input");
const searchDropdown = document.getElementById("search-dropdown");
let isHoveringDropdown = false;

searchInput.addEventListener("focusin", (e) => {
  searchDropdown.classList.add("animate-searchDropdownOpen");
  searchDropdown.classList.remove("animate-searchDropdownClose");
});

searchInput.addEventListener("focusout", (e) => {
  if (!isHoveringDropdown) {
    searchDropdown.classList.remove("animate-searchDropdownOpen");
    searchDropdown.classList.add("animate-searchDropdownClose");
  }
});

searchDropdown.addEventListener("mouseover", (e) => {
  isHoveringDropdown = true;
});

searchDropdown.addEventListener("mouseleave", (e) => {
  isHoveringDropdown = false;
  if (!(document.activeElement === searchInput)) {
    searchDropdown.classList.remove("animate-searchDropdownOpen");
    searchDropdown.classList.add("animate-searchDropdownClose");
  }
});

const renderNotification = (message, type) => {
  if (type === "error") {
    const errorNotification = document.getElementById("error-notification");
    const messageSpan = document.getElementById("error-notification-message");

    messageSpan.textContent = message;

    errorNotification.classList.add("right-6");
    errorNotification.classList.remove("-right-96");

    setTimeout(() => {
      errorNotification.classList.remove("right-6");
      errorNotification.classList.add("-right-96");
    }, 5000);
  }
};

// Input filter used for validation

// Restricts input for the given textbox to the given inputFilter function.
const setInputFilter = (textbox, inputFilter) => {
  //["input", "keydown", "keyup", "mousedown", "mouseup", "select", "contextmenu", "drop"].forEach(function (event) {
  textbox.addEventListener("input", function (e) {
    if (inputFilter(this.value) && this.value != 0) {
      // If a number was an input, it's safe to make the request to the server
      const callback = (error) => {
        if (!error) {
          // If success then mark the new number as an old number we can revert to if something fails.
          this.oldValue = this.value;
          this.oldSelectionStart = this.selectionStart;
          this.oldSelectionEnd = this.selectionEnd;
          return;
        } else if (this.hasOwnProperty("oldValue")) {
          this.value = this.oldValue;
          this.setSelectionRange(this.oldSelectionStart, this.oldSelectionEnd);
        } else {
          this.value = "";
        }
        // TODO: Display error notification
        renderNotification(error, "error");
      };

      const id = e.target.dataset.productId;
      updateCart(id, Number(e.target.value), callback);
      return;
    }

    if (this.hasOwnProperty("oldValue")) {
      this.value = this.oldValue;
      this.setSelectionRange(this.oldSelectionStart, this.oldSelectionEnd);
    } else {
      this.value = "";
    }
  });
};

function searchListener() {
  function handleForm(event) {
    event.target.form.submit();
  }
  document
    .getElementsByTagName("form")[0]
    .addEventListener("submit", handleForm);
}