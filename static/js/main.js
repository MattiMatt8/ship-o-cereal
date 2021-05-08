const CART_URL = "/cart/";
const cartTotalElement = document.getElementById("cart_total");

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
    axios.post(CART_URL + id + "/new/", {"quantity": quantity}, { headers: {"X-CSRFToken": CSRF_TOKEN }})
        .then((response) => {
            cartAddTotal(quantity);
            if (callback) {
                callback();
            }
        })
        .catch((error) => {
            console.log(error);
        });
}

function updateCart(id, quantity, callback=undefined) {
    axios.post(CART_URL + id + "/", {"quantity": quantity}, { headers: {"X-CSRFToken": CSRF_TOKEN }})
        .then((response) => {
            cartUpdateTotal(quantity, response.data.old_quantity);
            if (callback) {
                callback();
            }
        })
        .catch((error) => {
            console.log(error);
        });
}

function deleteFromCart(id, callback=undefined) {
    axios.post(CART_URL + id + "/delete/", null, { headers: {"X-CSRFToken": CSRF_TOKEN }})
        .then((response) => {
            cartDeleteFromTotal(response.data.quantity);
            if (callback) {
                callback();
            }
        })
        .catch((error) => {
            console.log(error);
        });
}

function cartAddTotal(quantity=1) {
    cartTotalElement.innerText = Number(cartTotalElement.innerText) + quantity;
}

function cartUpdateTotal(quantity, oldQuantity) {
    let newQuantity = quantity - Number(oldQuantity);
    cartTotalElement.innerText = Number(cartTotalElement.innerText) + newQuantity;
}

function cartDeleteFromTotal(quantity=1) {
    cartTotalElement.innerText = Number(cartTotalElement.innerText) - quantity;
}



// Searchbar

const searchInput = document.getElementById('search-input');
const searchDropdown = document.getElementById('search-dropdown');
let isHoveringDropdown = false;

searchInput.addEventListener('focusin', e =>{
    searchDropdown.classList.remove('max-h-0', 'overflow-hidden');
    searchDropdown.classList.add('max-h-64');

})

searchInput.addEventListener('focusout', e =>{
    if (!isHoveringDropdown) {
        searchDropdown.classList.add('max-h-0');
        searchDropdown.classList.remove('max-h-64');

    }
})

searchDropdown.addEventListener('mouseover', e =>{
    isHoveringDropdown = true;
})

searchDropdown.addEventListener('mouseleave', e =>{
    isHoveringDropdown = false;
    console.log("mouseleave!")
    if (!(document.activeElement === searchInput)) {
        searchDropdown.classList.add('max-h-0');
        searchDropdown.classList.remove('max-h-64');
    }
})

