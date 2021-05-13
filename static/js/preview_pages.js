const buttons = document.getElementsByClassName('buy-btn');

// Listen to all "add to cart" buttons
// If a user clicks on "add to cart" button, hide the button and unhide the incrementor/decrementor
Array.from(buttons).forEach(buyButton => {
    buyButton.addEventListener("click", (e) => {
        const id = Number(buyButton.dataset.productId);
        const amountSelect = buyButton.nextElementSibling;
        amountSelect.getElementsByTagName('input')[0].value = 1;

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
})

function decrement(e) {
    // A decrement function that fires when a user presses the minus button for a given product
    const btn = e.target.parentNode.parentElement.querySelector(
        'button[data-action="decrement"]'
    );
    const target = btn.nextElementSibling;
    let value = Number(target.value);
    const id = Number(target.dataset.productId);

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
        updateCart(id, Number(target.value) - 1, callback)
    } else {
        // Show buy now button and update cart
        const buyBtn = e.target.parentElement.parentElement.parentElement.parentElement.parentElement.querySelector('button');

        // If removal was successful, hide the incrementor/decrementor and unhide the "add to cart" button
        const callback = (error) => {
            if (error) {
                renderNotification(error, "error");
            } else {
                buyBtn.classList.remove('hidden');
                btn.parentElement.parentElement.parentElement.classList.add('hidden');
            }
        }
        deleteFromCart(id, callback)
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
            target.oldValue = value
        }
    };
    const id = target.dataset.productId;
    updateCart(id, Number(target.value) + 1, callback);
}

// Get all decrement buttons
const decrementButtons = document.querySelectorAll(
    `button[data-action="decrement"]`
);

// Get all increment buttons
const incrementButtons = document.querySelectorAll(
    `button[data-action="increment"]`
);

// Give decrement buttons their listener
decrementButtons.forEach((btn) => {
    btn.addEventListener("click", decrement);
});

// Give increment buttons their listener
incrementButtons.forEach((btn) => {
    btn.addEventListener("click", increment);
});

const inputAmountFields = document.getElementsByClassName('input-amount');

// Get all input amount fields (quantities) and setup their filters so users can only type integers
Array.from(inputAmountFields).forEach((item) => {
    // Initial value is given to let javascript revert back to a valid input
    item.oldValue = item.value;
    setInputFilter(item, function (value) {
        return /^[0-9]+$/.test(value);
    });
})
