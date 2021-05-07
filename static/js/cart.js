
const deleteButtons = document.getElementsByClassName('delete-btn');

for (let button of deleteButtons) {
    button.addEventListener('click', e =>{
        const id = Number(button.dataset.productId);
        const parent = document.getElementById(`product-id-${id}`);
        const deleteItem = () => parent.remove();

        deleteFromCart(id, callback=deleteItem)
    });
}

function getCartAmount(callback=undefined) {
    axios.get(MAIN_URL + "amount")
        .then((response) => {
            print(response.data)
            if (callback) {
                callback();
            }
        })
        .catch((error) => {
            console.log(error);
        });
}