const CHECKOUT_URL = "/checkout/";
const addressesInputs = document.getElementsByClassName("address-input");

for (let addressInput of addressesInputs) {
  addressInput.addEventListener("click", (e) => {
    const id = Number(addressInput.value);
    selectCard(id);
  });
}

function selectCard(id) {
  axios
    .post(CHECKOUT_URL + "address/" + id + "/", null, {
      headers: { "X-CSRFToken": CSRF_TOKEN },
    })
    .then((response) => {})
    .catch((error) => {
      console.log(error);
    });
}
