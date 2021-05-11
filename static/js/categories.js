function getProductsListener() {

    // Event delegation for fetching products
    function handleForm(event) {
        event.target.form.submit();
    }

    document.getElementsByTagName("form")[1]
        .addEventListener("change", handleForm);
}


// Wait for the DOM to load completely
document.addEventListener("DOMContentLoaded", function () {
    getProductsListener();
});