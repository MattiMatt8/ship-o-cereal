const amountSelect = document.getElementById("amount-btns");
const buyButton = document.getElementById("buy-btn");

buyButton.addEventListener("click", (e) => {
  const id = Number(buyButton.dataset.productId);

  const func = () => {
    buyButton.classList.add("hidden");
    amountSelect.classList.remove("hidden");
  };

  updateCart(id, 1, (callback = func));
});

function decrement(e) {
  const btn = e.target.parentNode.parentElement.querySelector(
    'button[data-action="decrement"]'
  );
  const target = btn.nextElementSibling;
  let value = Number(target.value);
  if (value > 1) {
    value--;
    target.value = value;
  } else {
    btn.disabled = true;
    btn.classList.remove(
      "cursor-pointer",
      "hover:text-gray-700",
      "hover:bg-gray-200"
    );
  }
}

function increment(e) {
  const btn = e.target.parentNode.parentElement.querySelector(
    'button[data-action="decrement"]'
  );
  const target = btn.nextElementSibling;
  let value = Number(target.value);
  value++;
  target.value = value;

  if (value === 2) {
    const leftBtn = e.target.parentNode.parentElement.querySelector(
      'button[data-action="decrement"]'
    );
    leftBtn.disabled = false;
    leftBtn.classList.add(
      "cursor-pointer",
      "hover:text-gray-700",
      "hover:bg-gray-200"
    );
  }
}

const decrementButtons = document.querySelectorAll(
  `button[data-action="decrement"]`
);

const incrementButtons = document.querySelectorAll(
  `button[data-action="increment"]`
);

decrementButtons.forEach((btn) => {
  btn.addEventListener("click", decrement);
});

incrementButtons.forEach((btn) => {
  btn.addEventListener("click", increment);
});
//addToCart(id, quantity);
