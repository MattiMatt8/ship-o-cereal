const CHECKOUT_URL = "/checkout/";
const nextEnabled = document.getElementById("next-enabled");
const nextDisabled = document.getElementById("next-disabled");
const textDisabled = document.getElementById("text-disabled");


function enableButton() {
  nextEnabled.classList.remove("hidden");
  nextDisabled.classList.add("hidden");
  textDisabled.classList.add("hidden");
}

function disableButton() {
  nextEnabled.classList.add("hidden");
  nextDisabled.classList.remove("hidden");
  textDisabled.classList.remove("hidden");
}