const MAIN_URL = "/cart/";
let cartTotalElement = document.getElementById("cart_total");

// Function getCookie from: https://docs.djangoproject.com/en/3.0/ref/csrf/#ajax
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const CSRF_TOKEN = getCookie('csrftoken');

function addToCart(id, quantity=1, callback=undefined) {
    axios.post(MAIN_URL + id + "/new", {"quantity": quantity}, { headers: {"X-CSRFToken": CSRF_TOKEN }})
        .then((response) => {
            cartUpdateTotal(quantity);
            if (callback) {
                callback();
            }
        })
        .catch((error) => {
            console.log(error);
        });
}

function updateCart(id, quantity, callback=undefined) {
    axios.post(MAIN_URL + id, {"quantity": quantity}, { headers: {"X-CSRFToken": CSRF_TOKEN }})
        .then((response) => {
            cartUpdateTotal(quantity);
            if (callback) {
                callback();
            }
        })
        .catch((error) => {
            console.log(error);
        });
}

function deleteFromCart(id, callback=undefined) {
    axios.post(MAIN_URL + id + "/delete", null, { headers: {"X-CSRFToken": CSRF_TOKEN }})
        .then((response) => {
            if (callback) {
                cartDeleteFromTotal(response.data.quantity);
                callback(response.data.quantity);
            }
        })
        .catch((error) => {
            console.log(error);
        });
}

function cartUpdateTotal(quantity=1) {
    cartTotalElement.innerText = Number(cartTotalElement.innerText) + quantity;
}

function cartDeleteFromTotal(quantity=1) {
    cartTotalElement.innerText = Number(cartTotalElement.innerText) - quantity;
}