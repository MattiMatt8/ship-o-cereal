// const amountSelect = document.getElementById('amount');
// const buyButton = document.getElementById('buy-btn');

// buyButton.addEventListener('click', e => {
//     const quantity = Number(amountSelect.value);
//     const id = Number(buyButton.dataset.productId);
//     updateCart(id, quantity)
// })

const buttons = document.getElementsByClassName('buy-btn');

Array.from(document.getElementsByClassName('buy-btn')).forEach(buyButton => {
    buyButton.addEventListener("click", (e) => {
        const id = Number(buyButton.dataset.productId);
        const amountSelect = buyButton.nextElementSibling;
        amountSelect.getElementsByTagName('input')[0].value = 1;
        const func = () => {
            buyButton.classList.add("hidden");
            amountSelect.classList.remove("hidden");
        };
        console.log("update cart")
        updateCart(id, 1, (callback = func));
    });

})


function decrement(e) {
    const btn = e.target.parentNode.parentElement.querySelector(
        'button[data-action="decrement"]'
    );
    const target = btn.nextElementSibling;
    let value = Number(target.value);
    if (value > 1) {
        value--;
        target.value = value;
        const id = target.dataset.productId;
        updateCart(id, Number(target.value))
    }
    if (value === 1) {
        btn.disabled = true;
        btn.classList.remove(
            "cursor-pointer",
            "hover:text-gray-700",
            "hover:bg-gray-200"
        );
        btn.classList.add("cursor-not-allowed")
    }
}

function increment(e) {
    const btn = e.target.parentNode.parentElement.querySelector(
        'button[data-action="decrement"]'
    );
    const target = btn.nextElementSibling;
    let value = Number(target.value);
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
        leftBtn.classList.remove("cursor-not-allowed")
    }
    const id = target.dataset.productId;
    updateCart(id, Number(target.value))
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
        //const target = e.target.nextElementSibling;
        const decrementBtn = e.target.previousElementSibling;
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
            decrementBtn.classList.remove("cursor-not-allowed")
        }
        updateCart(id, Number(e.target.value))


    })
})
