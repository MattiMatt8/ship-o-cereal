const addressesInputs = document.getElementsByClassName("address-input");

for (let addressInput of addressesInputs) {
  if (addressInput.checked === true) {
    enableButton();
  }
  addressInput.addEventListener("click", (e) => {
    const id = Number(addressInput.value);
    selectAddress(id);
  });
}

function selectAddress(id) {
  axios
    .post(CHECKOUT_URL + "address/" + id + "/", null, {
      headers: { "X-CSRFToken": CSRF_TOKEN },
    })
    .then((response) => {
      enableButton();
    })
    .catch((error) => {
      console.log(error);
    });
}