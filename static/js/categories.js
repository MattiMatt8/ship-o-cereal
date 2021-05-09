/* */
const getQueryString = () => {return window.location.search};
const categoryUrlPath = () => {return window.location.pathname};


function getProductsListener() {

    // Event delegation for fetching products
    function handleForm(event) {
        // event.preventDefault();
        event.target.form.submit();

    }
    document.getElementsByTagName("form")[1]
        .addEventListener("change", handleForm);
}


// Wait for the DOM to load completely
document.addEventListener("DOMContentLoaded", function () {
    getProductsListener();
});