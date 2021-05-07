function deleteItem(e) {
    console.log(e.target.parentNode.id);
}

document.getElementById("cart").addEventListener("click", deleteItem);
