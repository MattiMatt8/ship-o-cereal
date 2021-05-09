const cardInputs = document.getElementsByClassName("card-input");
let currentlySelectedCVC = null;
let currentlySelectedCVCmessage = null;
let buttonEnabled = false;

for (let cardInput of cardInputs) {
    let cvc = document.getElementById(`card-id-${cardInput.value}`);
    let cvcMessage = document.getElementById(`card-info-${cardInput.value}`);
    if (cardInput.checked == true) {
        cvc.value = "";
        cvc.classList.remove("hidden");
        cvcMessage.classList.remove("hidden");
        currentlySelectedCVC = cvc;
        currentlySelectedCVCmessage = cvcMessage;
    }
    cvc.addEventListener("keyup", (e) => {
        const cvcInfo = cvcMessage;
        if (cvc.value.length === 3) {
            let cvcNumber = Number(cvc.value);
            if (!isNaN(cvcNumber)) {
                enableButton();
                buttonEnabled = true;
                cvcInfo.classList.add("hidden");
            }
        } else {
            if (buttonEnabled) disableButton();
            if (currentlySelectedCVCmessage.classList.contains("hidden")) currentlySelectedCVCmessage.classList.remove("hidden");
        }
    });
    cardInput.addEventListener("click", (e) => {
        const id = Number(cardInput.value);
        const cvcField = cvc;
        const cvcInfo = cvcMessage;
        selectCard(id, cvcField, cvcInfo);
    });
}
// TODO: Select card automatically after it has been added
// TODO: Select address automatically after it has been added

// TODO: Store CVC code between pages?

// TODO: Travelling between views can't skip steps and confirmation stuff some for finished step

// TODO: Cart keep until order confirm
// TODO: Or recreate the cart?

function selectCard(id, cvcField, cvcInfo) {
    axios
        .post(CHECKOUT_URL + "card/" + id + "/", null, {
            headers: {"X-CSRFToken": CSRF_TOKEN},
        })
        .then((response) => {
            if (currentlySelectedCVC) {
                currentlySelectedCVC.classList.add("hidden");
                currentlySelectedCVC = cvcField;
                currentlySelectedCVCmessage.classList.add("hidden");
                currentlySelectedCVCmessage = cvcInfo;
            }
            cvcField.value = "";
            cvcField.classList.remove("hidden");
            cvcInfo.classList.remove("hidden");
        })
        .catch((error) => {
            console.log(error);
        });
}

// enableButton();
// Ting.length
// isNaN(Number(Ting))