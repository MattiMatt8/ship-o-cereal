// const amountSelect = document.getElementById('amount');
// const buyButton = document.getElementById('buy-btn');

// buyButton.addEventListener('click', e => {
//     const quantity = Number(amountSelect.value);
//     const id = Number(buyButton.dataset.productId);
//     updateCart(id, quantity)
// })

const buttons = document.getElementsByClassName('buy-btn');

for (let button of buttons) {
    button.addEventListener('click', e =>{
        const id = Number(button.dataset.productId);
        addToCart(id);
    });
}