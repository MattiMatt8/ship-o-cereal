// const amountSelect = document.getElementById('amount');
// const buyButton = document.getElementById('buy-btn');

// buyButton.addEventListener('click', e => {
//     const quantity = Number(amountSelect.value);
//     const id = Number(buyButton.dataset.productId);
//     updateCart(id, quantity)
// })

const buttons = document.getElementsByClassName('buy-btn');

const createIncrementor = (id, element) => {
    console.log(element);
    const parent = element.parentNode;
    element.remove();

    console.log(parent);

    parent.innerHTML += `
        <div class="text-customGray amountParent">
          <div class="custom-number-input w-30">
            <div class="flex flex-row h-10 w-full rounded-lg relative bg-transparent">
              <button
                  class="bg-gray-100 text-gray-600 h-full w-9 rounded-l outline-none cursor-pointer hover:text-gray-700 hover:bg-gray-200"
                  data-action="decrement"
                  type="button">
                <span class="m-auto text-2xl font-thin">−</span>
              </button>
              <input
                  type="text"
                  data-product-id="1"
                  class="outline-none focus:outline-none text-center w-10 bg-gray-100 font-semibold text-md flex items-center outline-none input-amount"
                  name="custom-input-number" value="1"/>
              <button data-action="increment"
                      class="bg-gray-100 text-gray-600 hover:text-gray-700 hover:bg-gray-200 h-full w-9 rounded-r cursor-pointer">
                <span class="m-auto text-2xl font-thin">+</span>
              </button>
            </div>
          </div>
        </div>
    
    `
}





for (let button of buttons) {
    button.addEventListener('click', e =>{
        const id = Number(button.dataset.productId);
        addToCart(id);
        buildBoi(id, button);

    });
}

