const deleteButtons = document.getElementsByClassName("delete-btn");
const productAmount = document.getElementById("product_amount");
const shippingAmount = document.getElementById("shipping_amount");
const totalAmount = document.getElementById("total_amount");

for (let button of deleteButtons) {
    // Adds event listeners to all add to cart buttons.
    button.addEventListener("click", (e) => {
        const id = Number(button.dataset.productId);
        const parent = document.getElementById(`product-id-${id}`);
        const deleteItem = () => {
            parent.remove();
            updateCartAmount();
        };
        deleteFromCart(id, (callback = deleteItem), true);
    });
}

function updateCartAmount() {
    // Sends request to the server to get the current amount everything
    // in his cart will cost and then updates it in the browser.
    axios
        .get(CART_URL + "amount")
        .then((response) => {
            // When success comes from the server it updates the numbers in the browser.
            let data = response.data.data;
            productAmount.innerText = `Products: \$${data.products_amount}`;
            shippingAmount.innerText = `Shipping: \$${data.shipping_amount}`;
            totalAmount.innerText = `\$${data.total_amount}`;
            // If there are no items left it changes the screen to display that there are no items in the cart.
            if (data.products_amount === 0) {
                document.getElementById("amount_box").classList.add("hidden");
                document.getElementById("cart_empty").classList.remove("hidden");
            }
        })
        .catch((error) => {
            console.log(error);
        });
}

function decrement(e) {
    // A decrement function that fires when a user presses the minus button for a given product
    const btn = e.target.parentNode.parentElement.querySelector(
        'button[data-action="decrement"]'
    );
    const target = btn.nextElementSibling;
    let value = Number(target.value);

    // Check if the quantity is at least bigger than 1
    // Else don't do anything
    if (value > 1) {

        // This function creates the behaviour for the frontend when it gets a response
        const callback = (error) => {
            // If an error occurs, display it to the user with a popup
            if (error) {
                renderNotification(error, "error");
            } else {
                // If the server responded without any errors we decrease the value
                value--;
                target.value = value;
                // If the value now is 1, we disable the button
                if (value === 1) {
                    btn.disabled = true;
                    btn.classList.remove(
                        "cursor-pointer",
                        "hover:text-gray-700",
                        "hover:bg-gray-200"
                    );
                    btn.classList.add("cursor-not-allowed");
                }
                // Update the cart value in the corner of the website
                updateCartAmount();
            }

        };
        // Get the id for the product that we want to decrease
        const id = target.dataset.productId;
        updateCart(id, Number(target.value) - 1, callback, true);
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
        // If an error occurs, display it to the user with a popup
        if (error) {
            renderNotification(error, "error");
        } else {
            // If the server responded without any errors we increase the value
            value++;
            target.value = value;
            // Check if the quantity is at least bigger than 1
            if (value > 1) {
                const leftBtn = e.target.parentNode.parentElement.querySelector(
                    'button[data-action="decrement"]'
                );
                leftBtn.disabled = false;
                leftBtn.classList.add(
                    "cursor-pointer",
                    "hover:text-gray-700",
                    "hover:bg-gray-200"
                );
                leftBtn.classList.remove("cursor-not-allowed");
            }
            updateCartAmount();
        }
    };
    const id = target.dataset.productId;
    updateCart(id, Number(target.value) + 1, callback, true);
}

const decrementButtons = document.querySelectorAll(
    `button[data-action="decrement"]`
);

const incrementButtons = document.querySelectorAll(
    `button[data-action="increment"]`
);

decrementButtons.forEach((btn) => {
    btn.addEventListener("click", decrement);
});

incrementButtons.forEach((btn) => {
    btn.addEventListener("click", increment);
});

// Restricts input for the given textbox to the given inputFilter function.


const inputAmountFields = document.getElementsByClassName("input-amount");

Array.from(inputAmountFields).forEach((item) => {
    setInputFilter(item, function (value) {
        return /^[0-9]+$/.test(value);
    });
    item.addEventListener("input", (e) => {
        const id = Number(item.dataset.productId);
        const decrementBtn = e.target.previousElementSibling;
        this.oldValue = this.value;

        if (e.target.value == 0) {
            e.target.value = 1;
        }
        if (e.target.value == 1) {
            decrementBtn.disabled = true;
            decrementBtn.classList.remove(
                "cursor-pointer",
                "hover:text-gray-700",
                "hover:bg-gray-200"
            );
            decrementBtn.classList.add("cursor-not-allowed");
        }
        if (e.target.value > 1) {
            decrementBtn.disabled = false;
            decrementBtn.classList.add(
                "cursor-pointer",
                "hover:text-gray-700",
                "hover:bg-gray-200"
            );
            decrementBtn.classList.remove("cursor-not-allowed");
        }
        updateCart(id, Number(e.target.value), updateCartAmount, true);
    });
});
