const amountSelect = document.getElementById("amount-btns");
const buyButton = document.getElementById("buy-btn");

buyButton.addEventListener("click", (e) => {
    const id = Number(buyButton.dataset.productId);

    const callback = (error) => {
        if (error) {
            // TODO: Display error message to user
        } else {
            buyButton.classList.add("hidden");
            amountSelect.classList.remove("hidden");
        }
    };

    updateCart(id, 1, callback);
});

function decrement(e) {
    const btn = e.target.parentNode.parentElement.querySelector(
        'button[data-action="decrement"]'
    );
    const target = btn.nextElementSibling;
    let value = Number(target.value);
    const id = Number(buyButton.dataset.productId);
    if (value > 1) {
        const callback = (error) => {
            if (error) {
                // TODO: Display error message to user
            } else {
                value--;
                target.value = value;
            }
        }
        updateCart(id, Number(target.value) - 1, callback);
    } else {
        // TODO: Show buy now button and updateCart(id, 0)

        const callback = (error) => {
            if (error) {
                // TODO: Display error message to user
            } else {
                buyButton.classList.remove("hidden");
                amountSelect.classList.add("hidden");
            }
        }

        deleteFromCart(id, callback);
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
            // TODO: Display error message to user
        } else {
            value++;
            target.value = value;

        }
    }

    const id = Number(buyButton.dataset.productId);
    updateCart(id, Number(target.value) + 1, callback)
}

const inputAmountField = document.getElementById('amount-input');

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
function setInputFilter(textbox, inputFilter) {
    ["input", "keydown", "keyup", "mousedown", "mouseup", "select", "contextmenu", "drop"].forEach(function (event) {
        textbox.addEventListener(event, function () {
            if (inputFilter(this.value)) {
                this.oldValue = this.value;
                this.oldSelectionStart = this.selectionStart;
                this.oldSelectionEnd = this.selectionEnd;
            } else if (this.hasOwnProperty("oldValue")) {
                this.value = this.oldValue;
                this.setSelectionRange(this.oldSelectionStart, this.oldSelectionEnd);
            } else {
                this.value = "";
            }
        });
    });
}

setInputFilter(inputAmountField, function (value) {
    return /^[0-9]+$/.test(value); // Allow digits and '.' only, using a RegExp
});

inputAmountField.addEventListener('input', (e) => {
    const id = Number(buyButton.dataset.productId);

    if (e.target.value == 0) {
        e.target.value = 1;
    }

    updateCart(id, Number(e.target.value));

})

//addToCart(id, quantity);
