const deleteButtons = document.getElementsByClassName("delete-btn");
const productAmount = document.getElementById("product_amount");
const shippingAmount = document.getElementById("shipping_amount");
const totalAmount = document.getElementById("total_amount");

for (let button of deleteButtons) {
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
    axios
        .get(CART_URL + "amount")
        .then((response) => {
            let data = response.data.data;
            productAmount.innerText = `Products: \$${data.products_amount}`;
            shippingAmount.innerText = `Shipping: \$${data.shipping_amount}`;
            totalAmount.innerText = `\$${data.total_amount}`;
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
    const btn = e.target.parentNode.parentElement.querySelector(
        'button[data-action="decrement"]'
    );
    const target = btn.nextElementSibling;
    let value = Number(target.value);
    if (value > 1) {
        const callback = (error) => {
            if (error) {
                renderNotification(error, "error");
            } else {
                value--;
                target.value = value;
                if (value === 1) {
                    btn.disabled = true;
                    btn.classList.remove(
                        "cursor-pointer",
                        "hover:text-gray-700",
                        "hover:bg-gray-200"
                    );
                    btn.classList.add("cursor-not-allowed");
                }
                updateCartAmount();
            }

        };
        const id = target.dataset.productId;
        updateCart(id, Number(target.value) - 1, callback, true);
    }

}

function increment(e) {
    const btn = e.target.parentNode.parentElement.querySelector(
        'button[data-action="decrement"]'
    );
    const target = btn.nextElementSibling;
    let value = Number(target.value);
    const callback = (error) => {
        if (error) {
            // TODO: Display an error notification with a message
            renderNotification(error, "error");
        } else {
            value++;
            target.value = value;

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

// inputAmountField.addEventListener('input', (e) => {
//     const id = Number(buyButton.dataset.productId);
//     updateCart(id, Number(e.target.value))
// })
