const CHECKOUT_URL = "/checkout/";
const nextEnabled = document.getElementById("next-enabled");
const nextDisabled = document.getElementById("next-disabled");
const textDisabled = document.getElementById("text-disabled");


function enableButton() {
  // Changes the button on the checkout page to enabled so the
  // user is then able to continue to the next page.
  nextEnabled.classList.remove("hidden");
  nextDisabled.classList.add("hidden");
  textDisabled.classList.add("hidden");
}

function disableButton() {
  // Changes the button on the checkout page to disabled so
  // we can prevent the user from continuing if he hasn't completed the step.
  nextEnabled.classList.add("hidden");
  nextDisabled.classList.remove("hidden");
  textDisabled.classList.remove("hidden");
}