const addressesInputs = document.getElementsByClassName("address-input");

for (let addressInput of addressesInputs) {
  if (addressInput.checked === true) {
    enableButton();
  }
  addressInput.addEventListener("click", (e) => {
    enableButton();
  });
}

window.addEventListener( "pageshow", (e) => {
  if (e.persisted || performance.getEntriesByType("navigation")[0].type === "back_forward") {
    for (let addressInput of addressesInputs) {
      if (addressInput.checked === true) {
        enableButton();
      }
    }
  }
});