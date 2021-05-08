const cardInputs = document.getElementsByClassName("card-input");
let currentlySelectedCVC = null;

for (let cardInput of cardInputs) {
  if (cardInput.checked == true) {
    let cvc = document.getElementById(`card-id-${cardInput.value}`);
    cvc.classList.remove("hidden");
    currentlySelectedCVC = cvc;
  }
  cardInput.addEventListener("click", (e) => {
    if (currentlySelectedCVC) {
      currentlySelectedCVC.classList.add("hidden");
    }
    const id = Number(cardInput.value);
    const cvcField = document.getElementById(`card-id-${id}`);
    cvcField.classList.remove("hidden");
    currentlySelectedCVC = cvcField;
    selectCard(id);
  });
}
// TODO: Cart selected in view when entering card site
// TODO: CVC when switching between cards
// TODO: Check if CVC has been filled to continue

// TODO: Travelling between views can't skip steps and confirmation stuff some for finished step

// TODO: Allow to press minus on amount to remove item completely
function selectCard(id) {
  axios
    .post(CHECKOUT_URL + "card/" + id + "/", null, {
      headers: { "X-CSRFToken": CSRF_TOKEN },
    })
    .then((response) => {
      enableButton();
    })
    .catch((error) => {
      console.log(error);
    });
}