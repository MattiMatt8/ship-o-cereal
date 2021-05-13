const amountSelect = document.getElementById("amount-btns");
const buyButton = document.getElementById("buy-btn");

// Listen to all "add to cart" buttons
// If a user clicks on "add to cart" button, hide the button and unhide the incrementor/decrementor
buyButton.addEventListener("click", (e) => {
    const id = Number(buyButton.dataset.productId);

    // A function that fires when a response has come from the server
    const callback = (error) => {
        if (error) {
            renderNotification(error, "error");

        } else {
            // Hide "add to cart"
            buyButton.classList.add("hidden");
            // Unhide increment/decrement
            amountSelect.classList.remove("hidden");
        }
    };

    updateCart(id, 1, callback);
});

function decrement(e) {
    // A decrement function that fires when a user presses the minus button for a given product
    const btn = e.target.parentNode.parentElement.querySelector(
        'button[data-action="decrement"]'
    );
    const target = btn.nextElementSibling;
    let value = Number(target.value);
    const id = Number(buyButton.dataset.productId);
    // If the value is larger than 1, then go ahead and decrement
    if (value > 1) {
        const callback = (error) => {
            if (error) {
                renderNotification(error, "error");
            } else {
                value--;
                target.value = value;
                // Oldvalue is used to revert back to if the user starts typing in non integers
                target.oldValue = value;
            }
        }
        updateCart(id, Number(target.value) - 1, callback);
    } else {
        // Show buy now button and update cart
        // If removal was successful, hide the incrementor/decrementor and unhide the "add to cart" button
        const callback = (error) => {
            if (error) {
                renderNotification(error, "error");
            } else {
                buyButton.classList.remove("hidden");
                amountSelect.classList.add("hidden");
            }
        }
        deleteFromCart(id, callback);
    }
}

function increment(e) {
    // An increment function that fires when a user presses the plus button for a given product
    const btn = e.target.parentNode.parentElement.querySelector(
        'button[data-action="decrement"]'
    );
    const target = btn.nextElementSibling;
    let value = Number(target.value);
    // This function creates the behaviour for the frontend when it gets a response
    const callback = (error) => {
        if (error) {
            renderNotification(error, "error");
        } else {
            value++;
            target.value = value;
            // Oldvalue is used to revert back to if the user starts typing in non integers
            target.oldValue = value;
        }
    }

    const id = Number(buyButton.dataset.productId);
    updateCart(id, Number(target.value) + 1, callback)
}

const inputAmountField = document.getElementById('amount-input');

// Get all decrement buttons
const decrementButtons = document.querySelectorAll(
    `button[data-action="decrement"]`
);

// Get all increment buttons
const incrementButtons = document.querySelectorAll(
    `button[data-action="increment"]`
);

// Give all decrement buttons their listener
decrementButtons.forEach((btn) => {
    btn.addEventListener("click", decrement);
});

// Give all increment buttons their listener
incrementButtons.forEach((btn) => {
    btn.addEventListener("click", increment);
});

// Restricts input for the given textbox to the given inputFilter function.
inputAmountField.oldValue = inputAmountField.value;

setInputFilter(inputAmountField, function (value) {
    return /^[0-9]+$/.test(value); // Allow digits and '.' only, using a RegExp
});


