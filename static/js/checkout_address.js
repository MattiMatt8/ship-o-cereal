const addressesInputs = document.getElementsByClassName("address-input");

for (let addressInput of addressesInputs) {
  // Allows user to continue if there was already a address selected.
  if (addressInput.checked === true) {
    enableButton();
  }
  // Adds event listeners to the address selection, so when
  // an address is selected it allows them to continue.
  addressInput.addEventListener("click", (e) => {
    enableButton();
  });
}

window.addEventListener( "pageshow", (e) => {
  // Event listener which watches if the user goes back a page in the checkout, so if he does
  // it checks the option he had previously selected on that page.
  if (e.persisted || performance.getEntriesByType("navigation")[0].type === "back_forward") {
    for (let addressInput of addressesInputs) {
      // Selects a address if it has already been selected.
      if (addressInput.checked === true) {
        enableButton();
      }
    }
  }
});