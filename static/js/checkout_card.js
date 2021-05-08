const cardInputs = document.getElementsByClassName("card-input");

for (let cardInput of cardInputs) {
  cardInput.addEventListener("click", (e) => {
    const id = Number(cardInput.value);
    const cvcField = document.getElementById(`card-id-${id}`);
    cvcField.classList.remove("hidden");
    selectCard(id);
  });
}
// TODO: Cart selected in view when entering card site
// TODO: CVC when switching between cards
// TODO: Check if CVC has been filled to continue

// TODO: Travelling between views can't skip steps and confirmation stuff some for finished step
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