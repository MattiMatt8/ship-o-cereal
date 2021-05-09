// const amountSelect = document.getElementById('amount');
// const buyButton = document.getElementById('buy-btn');

// buyButton.addEventListener('click', e => {
//     const quantity = Number(amountSelect.value);
//     const id = Number(buyButton.dataset.productId);
//     updateCart(id, quantity)
// })

const buttons = document.getElementsByClassName('buy-btn');

Array.from(buttons).forEach(buyButton => {
    buyButton.addEventListener("click", (e) => {
        const id = Number(buyButton.dataset.productId);
        const amountSelect = buyButton.nextElementSibling;
        amountSelect.getElementsByTagName('input')[0].value = 1;
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

})

function decrement(e) {
    const btn = e.target.parentNode.parentElement.querySelector(
        'button[data-action="decrement"]'
    );
    const target = btn.nextElementSibling;
    let value = Number(target.value);
    const id = target.dataset.productId;
    if (value > 1) {
        const callback = (error) => {
            if (error) {
                // TODO: Display error message to user
            } else {
                value--;
                target.value = value;
            }
        }

        updateCart(id, Number(target.value) - 1, callback)
    } else {
        // Show buy now button and updateCart(id, 0)
        const buyBtn = e.target.parentElement.parentElement.parentElement.parentElement.parentElement.querySelector('button');

        const callback = (error) => {
            if (error) {
                // TODO: Display error message to user

            } else {
                buyBtn.classList.remove('hidden');
                btn.parentElement.parentElement.parentElement.classList.add('hidden');
            }

        }

        deleteFromCart(id, callback)
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
        }
    };
    const id = target.dataset.productId;
    updateCart(id, Number(target.value) + 1, callback);
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

const inputAmountFields = document.getElementsByClassName('input-amount');

Array.from(inputAmountFields).forEach((item) => {
    setInputFilter(item, function (value) {
        return /^[0-9]+$/.test(value);
    });
    item.addEventListener('input', (e) => {
        const id = Number(item.dataset.productId);
        if (e.target.value == 0) {
            e.target.value = 1;
        }
        updateCart(id, Number(e.target.value))
    })
})
