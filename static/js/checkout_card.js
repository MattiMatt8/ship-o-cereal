const cardInputs = document.getElementsByClassName("card-input");
let currentlySelectedCVC = null;
let currentlySelectedCVCmessage = null;
let buttonEnabled = false;

for (let cardInput of cardInputs) {
    let cvc = document.getElementById(`card-id-${cardInput.value}`);
    let cvcMessage = document.getElementById(`card-info-${cardInput.value}`);
    if (cardInput.checked == true) {
        // If a card has been selected it unhides all its elements
        cvc.value = "";
        cvc.classList.remove("hidden");
        cvc.disabled = false;
        cvcMessage.classList.remove("hidden");
        currentlySelectedCVC = cvc;
        currentlySelectedCVCmessage = cvcMessage;
    }
    cvc.addEventListener("keyup", (e) => {
        const cvcInfo = cvcMessage;
        if (cvc.value.length === 3) {
            // If the cvc is valid it unlocks the option to continue to the next page.
            let cvcNumber = Number(cvc.value);
            if (!isNaN(cvcNumber)) {
                enableButton();
                buttonEnabled = true;
                cvcInfo.classList.add("hidden");
                cvc.classList.remove("border-customRed");
                cvc.classList.add("border-customGreen");
            }
        } else {
            // If the cvc is invalid it disables the option to continue to the next page.
            if (buttonEnabled) disableButton();
            if (currentlySelectedCVCmessage.classList.contains("hidden")) currentlySelectedCVCmessage.classList.remove("hidden");
            cvc.classList.remove("border-customGreen");
            cvc.classList.add("border-customRed");
        }
    });
    // Listener so when the card is pressed in unhides the cvc field
    // for that card and hides the cvc field for the previously selected card.
    cardInput.addEventListener("click", (e) => {
        const cvcField = cvc;
        const cvcInfo = cvcMessage;
        if (currentlySelectedCVC) {
            currentlySelectedCVC.classList.add("hidden");
            currentlySelectedCVC.disabled = true;
            currentlySelectedCVCmessage.classList.add("hidden");
        }
        cvcField.value = "";
        cvcField.classList.remove("hidden");
        cvcField.disabled = false;
        cvcInfo.classList.remove("hidden");
        currentlySelectedCVC = cvcField;
        currentlySelectedCVCmessage = cvcInfo;
    });
}

window.addEventListener( "pageshow", (e) => {
  // Event listener which watches if the user goes back a page in the checkout, so if he does
  // it checks the option he had previously selected on that page.
  if (e.persisted || performance.getEntriesByType("navigation")[0].type === "back_forward") {
    for (let cardInput of cardInputs) {
      // Selects a card if it has already been selected.
      if (cardInput.checked === true) {
        let cvc = document.getElementById(`card-id-${cardInput.value}`);
        cvc.classList.remove("hidden");
        cvc.disabled = false;
        cvc.value = "";
      }
    }
  }
});
