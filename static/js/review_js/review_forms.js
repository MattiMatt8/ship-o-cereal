function newFormContainer () {
     // Create a new div & set the attributes
    let container = document.createElement("div");
    container.setAttribute("class", "mt-5");

    return container;
}

function getNewReviewForm() {
    // Returns a div containing a form to add a new review

    // Container for adding a new review
    let divTag = newFormContainer();
    divTag.setAttribute("id", "new-review");

    // Add a form for creating a new review
    divTag.innerHTML = `
        <form method="post" class="flex flex-col md:w-full lg:w-2/3 xl:w-9/12 2xl:w-10/12" id="new-review-form">
          <h2 class="text-lg mb-2">Please leave a review.</h2>
          <div class="mb-1">
            <label for="id_title"
                   class="block text-gray-700 text-base mb-1">Title</label>
            <input type="text" name="title"
                   class="border border-customGray rounded px-4 shadow-inner w-full h-8 placeholder-gray-300 focus:outline-none"
                   maxlength="255" required="" id="id_title" placeholder="It was...">
          </div>
          <div class="mb-3">
            <label for="id_stars"
                   class="block text-gray-700 text-base mb-1">Stars</label>   
            <div class="flex flex-row">
              ${getFormStars(1)}
              <input value="1" type="number" name="stars" class="hidden" step="any" required="" id="id_stars">
            </div>
          </div>
          <div class="mb-3">
            <label for="id_review"
                   class="block text-gray-700 text-base mb-1">Review</label>
            <textarea name="review" cols="40" rows="5"
                      class="border border-customGray rounded py-4 px-4 shadow-inner w-full placeholder-gray-300 focus:outline-none"
                      placeholder="I thought it was... because..." maxlength="500" required=""
                      id="id_review"></textarea>
          </div>
          <div class="flex justify-end mb-3 lg:mb-10">
            <button
                class="bg-customBlue hover:shadow-md rounded text-customViolet text-base w-32 py-1 px-4 focus:outline-none"
                type="submit">Post review
            </button>
          </div>
        </form>`;

    return divTag;
};

function getUpdateReviewForm(id, title, stars, review) {
    /* Returns a div containing a form to update a review
     with all the old information in it. */

    // Container for adding a new review
    let divTag = newFormContainer();
    divTag.setAttribute("id", "update-review");

    // Add a form for updating a current review
    divTag.innerHTML = `
        <form method = "post" class="flex flex-col md:w-full lg:w-2/3 xl:w-9/12 2xl:w-10/12" id="new-review-form">
          <div class="mb-1">
            <label for="id_title"
                   class="block text-gray-700 text-base mb-1">Title</label>     
            <input type="text" name="title" value="${title}"
                   class="border border-customGray rounded px-4 shadow-inner w-full h-8 placeholder-gray-300 focus:outline-none"
                   maxlength="255" required="" id="id_title">
          </div>
          <div class="mb-3">
            <label for="id_stars"
                   class="block text-gray-700 text-base mb-1">Stars</label>
            <div class="flex flex-row">
              ${getFormStars(Number(stars))}
              <input value="${stars}" type="number" name="stars" class="hidden" step="any" required="" id="id_stars">
            </div>
          </div>
          <div class="mb-3">
            <label for="id_review"
                   class="block text-gray-700 text-base mb-1">Review</label>
            <textarea name="review" cols="40" rows="5"
                      class="border border-customGray rounded py-4 px-4 shadow-inner w-full placeholder-gray-300 focus:outline-none"
                      maxlength="500" required="" id="id_review">${review}</textarea>
            </div>
          <div class="flex justify-between mb-3">
            <button id="review-update-cancel"
                    class="text-center text-base text-customViolet rounded border border-customViolet py-1 px-4 focus:outline-none hover:shadow-md"
                    type="button" data-review-id="${id}">Cancel
            </button>
            <button
                class="bg-customBlue hover:shadow-md rounded text-customViolet text-base w-36 py-1 px-4 focus:outline-none"
                type="submit">Update review
            </button>
          </div>
        </form>`;

    return divTag
}