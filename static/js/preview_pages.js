// const amountSelect = document.getElementById('amount');
// const buyButton = document.getElementById('buy-btn');

// buyButton.addEventListener('click', e => {
//     const quantity = Number(amountSelect.value);
//     const id = Number(buyButton.dataset.productId);
//     updateCart(id, quantity)
// })

const buttons = document.getElementsByClassName('buy-btn');


for (let button of buttons) {
    button.addEventListener('click', e => {
        const id = Number(button.dataset.productId);
        addToCart(id);

    });
}

Array.from(document.getElementsByClassName('buy-btn')).forEach(buyButton => {
    buyButton.addEventListener("click", (e) => {
        const id = Number(buyButton.dataset.productId);
        const amountSelect = buyButton.nextElementSibling;
        amountSelect.getElementsByTagName('input')[0].value = 1;
        const func = () => {
            buyButton.classList.add("hidden");
            amountSelect.classList.remove("hidden");
        };

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
        console.log(`Gonna send in updateCart(${id}, ${Number(target.value)})})`);
        updateCart(id, Number(target.value))
    } else {
        btn.disabled = true;
        btn.classList.remove(
            "cursor-pointer",
            "hover:text-gray-700",
            "hover:bg-gray-200"
        );
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

    if (value === 2) {
        const leftBtn = e.target.parentNode.parentElement.querySelector(
            'button[data-action="decrement"]'
        );
        leftBtn.disabled = false;
        leftBtn.classList.add(
            "cursor-pointer",
            "hover:text-gray-700",
            "hover:bg-gray-200"
        );
    }
    const id = target.dataset.productId;
    console.log(`Gonna send in updateCart(${id}, ${Number(target.value)})})`);
    updateCart(id, Number(target.value))
}

const decrementButtons = document.querySelectorAll(
    `button[data-action="decrement"]`
);

const incrementButtons = document.querySelectorAll(
    `button[data-action="increment"]`
);


decrementButtons.forEach((btn) => {
    console.log("decrement!")
    btn.addEventListener("click", decrement);
});

incrementButtons.forEach((btn) => {
    console.log("increment!")
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
        updateCart(id, Number(e.target.value))
    })
})
