const CART_URL = "/cart/";
const cartTotalElement = document.getElementById("cart_total");
let cartTotal = Number(cartTotalElement.innerText);

// Searchbar variables
const searchForm = document.getElementById('search-form');
const searchInput = document.getElementById("search-input");
const searchDropdown = document.getElementById("search-dropdown");
let isHoveringDropdown = false;

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

function updateCart(id, quantity, callback = undefined, in_cart = false) {
    axios
        .post(
            CART_URL + id + "/",
            {quantity: quantity, in_cart: in_cart},
            {headers: {"X-CSRFToken": CSRF_TOKEN}}
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
            {in_cart: in_cart},
            {headers: {"X-CSRFToken": CSRF_TOKEN}}
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

function deleteSearch(id, callback = undefined) {
    axios
        .post(
            "/profile/search/" + id + "/delete/",
            null,
            {headers: {"X-CSRFToken": CSRF_TOKEN}}
        )
        .then((response) => {
            if (callback) {
                callback();
            }
        })
        .catch((error) => {
            console.log(error);
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

const renderNotification = (object, type) => { // Render a notification to be displayed for the user
    if (type === "error") {
        const errorNotification = document.getElementById("error-notification");
        const messageSpan = document.getElementById("error-notification-message");

        messageSpan.textContent = object.response.data.message;

        errorNotification.classList.add("right-6");
        errorNotification.classList.remove("-right-96");

        setTimeout(() => {
            errorNotification.classList.remove("right-6");
            errorNotification.classList.add("-right-96");
        }, 5000);
    }
};

// Listen for a search from search history dropdown
function searchFromHistoryListener () {
    let searchTermButtons = document.getElementsByClassName('search-term-button');

    Array.from(searchTermButtons).forEach(btn => {
        btn.addEventListener("click", () => window.location.href = `/search/${btn.dataset.searchValue}`
        );
    })

    // Only available for users, search dropdown is not rendered for non-users
    if (searchDropdown) {
        // When a logged in user focuses on the search bar, a dropdown list with their search history should happen
        searchInput.addEventListener("focusin", (e) => {
            searchDropdown.classList.add("animate-searchDropdownOpen");
            searchDropdown.classList.remove("animate-searchDropdownClose");
        });

        // If user is no longer focusing on search input, only hide the dropdown if he's not hovering over it
        searchInput.addEventListener("focusout", (e) => {
            if (!isHoveringDropdown) {
                searchDropdown.classList.remove("animate-searchDropdownOpen");
                searchDropdown.classList.add("animate-searchDropdownClose");
            }
        });

        // Listen if user enters the dropdown and set isHoveringDropdown to true
        searchDropdown.addEventListener("mouseover", (e) => {
            isHoveringDropdown = true;
        });

        // Listen if user leaves the dropdown and set isHoveringDropdown to false, but only remove the
        // dropdown if he's not focused on the input
        searchDropdown.addEventListener("mouseleave", (e) => {
            isHoveringDropdown = false;
            if (!(document.activeElement === searchInput)) {
                searchDropdown.classList.remove("animate-searchDropdownOpen");
                searchDropdown.classList.add("animate-searchDropdownClose");
            }
        });
    };
};

// Listen for search by text input
function searchBarListener () {

    // Handle search submission
    function submitSearch(event) {
        // Redirects the user to the search page when he searches
        event.preventDefault();
        window.location.href = `/search/${searchInput.value}`;
    }
    searchForm.addEventListener("submit", submitSearch);
};

// Listen for deleting an entry from search history
function deleteSearchButtonListener () {

    // Search history entries contained in a list with a delete button
    let searchDeleteButtons = document.getElementsByClassName(".search-delete-button");

    // Add an event listener to each delete button
    Array.from(searchDeleteButtons).forEach(btn => {
        btn.addEventListener('click', e => {
            let id = btn.dataset.searchId;

            // Callback function for further request
            let callback = (error) => {
                if (!error) {
                    // Manipulate DOM based on num of search entries available
                    let numOfListItemsAfterDelete = searchEntryList.childElementCount - 1;

                    // If search history is empty this should remove the whole dropdown box
                    if (numOfListItemsAfterDelete === 0) {
                        searchDropdown.classList.add('hidden');

                    }
                    else {
                        // If search entry deletion was successful, remove from DOM
                        btn.parentElement.remove();
                    }
                }
            };
        // Call axios request with call back
        deleteSearch(id, callback);
        })
    });
};

// Wait for the DOM to load completely
document.addEventListener("DOMContentLoaded", () => {

    // Listeners
    searchBarListener();
    deleteSearchButtonListener();
    searchFromHistoryListener();
});
