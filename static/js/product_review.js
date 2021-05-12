const starButtons = document.getElementsByClassName("star-btn");
const starInput = document.getElementById("id_stars");
let stopHoverMove = false;

// -- Review star functionality --

for (let starButton of starButtons) {
    // Adds event listeners to the review stars
    starButton.addEventListener("mouseover", starHover);
    starButton.addEventListener("click", starPress);
}

function changeStars(starNum) {
    // Makes it so when you hover over stars or press on them they change to either
    // filled stars or unfilled stars based on where you hover or click.
    for (i=1; i <= 5; i++) {
        let starFilled = document.getElementById(`star-filled-${i}`);
        let starUnfilled = document.getElementById(`star-unfilled-${i}`);
        starInput.value = starNum;
        if (i <= starNum) {
            if (starFilled.classList.contains("hidden")) {
                starUnfilled.classList.add("hidden");
                starFilled.classList.remove("hidden");
            }
        }
        else {
            if (starUnfilled.classList.contains("hidden")) {
                starFilled.classList.add("hidden");
                starUnfilled.classList.remove("hidden");
            }
        }
    }
}

function starHover(event) {
    // When hovered over it calls the function change stars
    // unless a star has been pressed on then it does nothing
    if (stopHoverMove) return;
    changeStars(event.currentTarget.value);
}

function starPress(event) {
    // When a stared is pressed it either changes it so they stop changing
    // when being hovered over but only when pressed on.
    if (stopHoverMove) {
        changeStars(event.currentTarget.value);
    }
    stopHoverMove = true;
}
;


// -- Review add, update & delete calls --

// Event listener for the submit of a new review
addSubmitListener("new-review-form")

function addSubmitListener(elementId, callback) {
    // Adds a submit listener if the element exists
    let element = document.getElementById(elementId);
    if (element) {
        element.addEventListener("submit", submitReview);
    }
}

function submitReview(event) {
    // When a new review is submitted, send to the server the request and if it's
    // successful it will then update the view for the user with his newly created review.
    event.preventDefault();
    let stars = document.getElementById("id_stars").value;
    let title = document.getElementById("id_title").value;
    let review = document.getElementById("id_review").value;
    axios
        .post(
            "reviews/new/",
            {stars: stars, title: title, review: review},
            {headers: {"X-CSRFToken": CSRF_TOKEN}}
        )
        .then((response) => {
            document.getElementById("new-review").classList.add("hidden");
            console.log("Full name: " + response.data.data.full_name); // TODO: Change
            console.log("Image: " + response.data.data.profile_image); // TODO: Change
        })
        .catch((error) => {
            console.log(error);
        });
}

function getUpdateReviewForm(title, stars, review) {
    // Returns a form to update a review with and with all the old information in it.
    return `
        <div class="w-9/12 mt-5" id="update-review">
          <h2 class="text-lg mb-2">Please leave a review.</h2>
          <form method="post" class="flex flex-col" id="new-review-form">
            {% csrf_token %}
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
                ${getStars(stars)}
                <input value="1" type="number" name="stars" class="hidden" step="any" required="" id="id_stars">
              </div>
            </div>
            <div class="mb-3">
              <label for="{{ form.review.id_for_label }}"
                     class="block text-gray-700 text-base mb-1">Review</label>
              <textarea name="review" cols="40" rows="5" value="${review}"
                        class="border border-customGray rounded py-4 px-4 shadow-inner w-full placeholder-gray-300 focus:outline-none"
                        maxlength="500" required="" id="id_review"></textarea>
            </div>
            <div class="flex justify-end mb-3">
              <button class="bg-customBlue hover:shadow-md rounded text-customViolet text-base w-32 py-1 px-4 focus:outline-none"
                      type="submit">Update review
              </button>
            </div>
          </form>
        </div>
        `;
}

function getStars(totalStars) {
    // Returns stars and with the correct stars hidden
    // based on the total stars parameter.
    let stars = ""
    for (let i=1; i <= 5; i++) {
        if (i === 1) stars += getFilledStar(i);
        if (i <= totalStars) {
            stars += getUnfilledStar(i,true);
            stars += getFilledStar(i);
        }
        else {
            stars += getUnfilledStar(i);
            stars += getFilledStar(i, true);
        }
    }
    return stars;
}

function getFilledStar(id, hidden=false) {
    // Returns a filled star either with the correct id and hidden or not.
    hidden = hidden ? "class='hidden'" : "";
    return `<button type="button" value="${id}" class="star-btn focus:outline-none">
            <svg id="star-filled-${id} ${hidden} width="22" height="21" viewBox="0 0 22 21" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M11.2204 4.06848L12.7268 7.86637L13.0694 8.73021L13.9955 8.80806L18.0654 9.15022L14.9115 11.9833L14.2557 12.5723L14.4512 13.4319L15.3914 17.5652L12.0295 15.4119L11.2204 14.8937L10.4114 15.4119L7.04945 17.5652L7.98967 13.4319L8.1852 12.5723L7.52942 11.9833L4.37555 9.15022L8.44542 8.80806L9.37146 8.73021L9.71409 7.86637L11.2204 4.06848Z" fill="#F1C644" stroke="#F1C644" stroke-width="3"/>
            </svg></button>`;
}

function getUnfilledStar(id, hidden=false) {
    // Returns a unfilled star either with the correct id and hidden or not.
    hidden = hidden ? "class='hidden'" : "";
    return `<button type="button" value="${id}" class="star-btn focus:outline-none">
            <svg id="star-unfilled-${id}" ${hidden} width="22" height="21" viewBox="0 0 22 21" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M11.0344 0L13.9351 7.31334L21.4642 7.9463L15.7278 13.0992L17.4804 20.8037L11.0344 16.675L4.58844 20.8037L6.341 13.0992L0.604612 7.9463L8.13373 7.31334L11.0344 0Z" fill="#D4D4D4"/>
            </svg></button>`;
}

function changeReview(event) {
    // When a new review is changed, send the new state of the review to
    // the server and if successful change the review to the newly edited one.
    event.preventDefault();
    let stars = document.getElementById("id_stars").value;
    let title = document.getElementById("id_title").value;
    let review = document.getElementById("id_review").value;
    axios
        .post(
            "reviews/update/",
            {stars: stars, title: title, review: review},
            {headers: {"X-CSRFToken": CSRF_TOKEN}}
        )
        .then((response) => {
            document.getElementById("new-review").classList.add("hidden");
            console.log("Full name: " + response.data.data.full_name);
            console.log("Image: " + response.data.data.profile_image);
        })
        .catch((error) => {
            console.log(error);
        });
}