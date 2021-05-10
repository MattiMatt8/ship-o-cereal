const addressesInputs = document.getElementsByClassName("address-input");

for (let addressInput of addressesInputs) {
  if (addressInput.checked === true) {
    enableButton();
  }
  addressInput.addEventListener("click", (e) => {
    const id = Number(addressInput.value);
    enableButton();
  });
}