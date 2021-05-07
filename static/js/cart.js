
const deleteButtons = document.getElementsByClassName('delete-btn');

for (let button of deleteButtons) {
    button.addEventListener('click', e =>{
        const id = Number(button.dataset.productId);
        const parent = document.getElementById(`product-id-${id}`);
        const deleteItem = () => parent.remove();

        deleteFromCart(id, 0, callback=deleteItem)
    });
}
