const buttons = document.getElementsByClassName('buy-btn');

Array.from(buttons).forEach(buyButton => {
    buyButton.addEventListener("click", (e) => {
        const id = Number(buyButton.dataset.productId);
        const amountSelect = buyButton.nextElementSibling;
        amountSelect.getElementsByTagName('input')[0].value = 1;
        const callback = (error) => {
            if (error) {
                // TODO: Display error message to user
                renderNotification(error, "error");
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
    const id = Number(target.dataset.productId);
    if (value > 1) {
        const callback = (error) => {
            if (error) {
                // TODO: Display error message to user
                renderNotification(error, "error");
            } else {
                value--;
                target.value = value;
                target.oldValue = value;
            }
        }
        updateCart(id, Number(target.value) - 1, callback)
    } else {
        // Show buy now button and updateCart(id, 0)
        const buyBtn = e.target.parentElement.parentElement.parentElement.parentElement.parentElement.querySelector('button');

        const callback = (error) => {
            if (error) {
                // TODO: Display error message to user
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
            target.oldValue = value
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

const inputAmountFields = document.getElementsByClassName('input-amount');

Array.from(inputAmountFields).forEach((item) => {
    item.oldValue = item.value;
    setInputFilter(item, function (value) {
        return /^[0-9]+$/.test(value);
    });
})
