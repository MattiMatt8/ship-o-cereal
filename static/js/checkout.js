const CHECKOUT_URL = "/checkout/";
const addresses = document.getElementsByClassName("address-option");
console.log(addresses)
for (let address of addresses) {
    console.log("huhfff")

    address.addEventListener('click', e =>{
        const id = Number(address.dataset.addressId);
        selectCard(id);
    });
}

function selectCard(id) {
    axios.post(CHECKOUT_URL + "address/" + id + "/", null, { headers: {"X-CSRFToken": CSRF_TOKEN }})
        .then((response) => {
            console.log("success");
        })
        .catch((error) => {
            console.log(error);
        });
}