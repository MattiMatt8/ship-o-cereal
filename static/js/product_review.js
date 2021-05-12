// -- Review star functionality --
let starInput;
let stopHoverMove;

// If there is a new review form this will add the stars to it
addListenersToStars();

function addListenersToStars() {
    // Adds listeners to the review stars so they function properly when hovered over.
    let starButtons = document.getElementsByClassName("star-btn");
    starInput = document.getElementById("id_stars");
    stopHoverMove = false;
    for (let starButton of starButtons) {
        starButton.addEventListener("mouseover", starHover);
        starButton.addEventListener("click", starPress);
    }
}

function changeStars(starNum) {
    // Makes it so when you hover over stars or press on them they change to either
    // filled stars or unfilled stars based on where you hover or click.
    for (i = 1; i <= 5; i++) {
        let starFilled = document.getElementById(`star-filled-${i}`);
        let starUnfilled = document.getElementById(`star-unfilled-${i}`);
        starInput.value = starNum;
        if (i <= starNum) {
            if (starFilled.classList.contains("hidden")) {
                starUnfilled.classList.add("hidden");
                starFilled.classList.remove("hidden");
            }
        } else {
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
addSubmitListener("new-review-form", submitNewReview);

function addSubmitListener(elementId, callback) {
    // Adds a submit listener if the element exists
    let element = document.getElementById(elementId);
    if (element) {
        element.addEventListener("submit", callback);
    }
}

function submitReview(event, url, callback) {
    // When a review is submitted, send to the server the request and if it's
    // successful it will call the callback function.
    event.preventDefault();
    let title = document.getElementById("id_title").value;
    let stars = document.getElementById("id_stars").value;
    let review = document.getElementById("id_review").value;
    axios
        .post(
            `reviews/${url}/`,
            {stars: stars, title: title, review: review},
            {headers: {"X-CSRFToken": CSRF_TOKEN}}
        )
        .then((response) => {
            callback(response.data.data);
        })
        .catch((error) => {
            console.log(error);
        });
}

function submitNewReview(event) {
    submitReview(event, "new", renderNewReview);
}

function renderNewReview(data) {
    // Renders the new review for the user and removes the form it was submitted in.
    // TODO: Check if this works if there are no reviews
    // TODO: Change header title if there are no reviews to Rreviews instead of that there are no reviews
    let newReview = getReviewFilled(data.id, data.title, data.stars, data.review, data.profile_image, data.date, data.full_name);
    let reviewsHeader = document.getElementById("reviews-header");
    document.getElementById("new-review-form").remove();
    reviewsHeader.parentNode.insertBefore(newReview, reviewsHeader.nextSibling);
    addClickListener("change-review", renderUpdateReviewForm);
}

function submitUpdateReview(event) {
    submitReview(event, "update", undefined);
}

function getReviewFilled(id, title, stars, review, picture, date, fullName) {
    // Returns a review formatted with everything filled out and ready.
    let divTag = document.createElement("div");
    divTag.setAttribute("class", "flex flex-row mt-8");
    divTag.setAttribute("id", `review-${id}`);
    if (picture) {
        html_picture = `<img className="w-16 h-16 rounded-full object-cover object-center" src="${picture}">`;
    } else {
        html_picture = `<div class="bg-customGray rounded-full w-16 h-16 flex justify-center items-center">
                        <svg width="36" height="36" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <path d="M30.1817 26.8453C29.5185 25.2744 28.5561 23.8475 27.3481 22.6441C26.1438 21.4373 24.7171 20.475 23.147 19.8105C23.1329 19.8035 23.1188 19.8 23.1048 19.793C25.295 18.2109 26.7188 15.634 26.7188 12.7266C26.7188 7.91016 22.8165 4.00781 18.0001 4.00781C13.1837 4.00781 9.28134 7.91016 9.28134 12.7266C9.28134 15.634 10.7052 18.2109 12.8954 19.7965C12.8813 19.8035 12.8673 19.807 12.8532 19.8141C11.2782 20.4785 9.86493 21.4312 8.65204 22.6477C7.44516 23.852 6.48292 25.2786 5.81845 26.8488C5.16567 28.386 4.81362 30.0341 4.78134 31.7039C4.7804 31.7414 4.78698 31.7788 4.80069 31.8137C4.81441 31.8486 4.83498 31.8805 4.86119 31.9073C4.8874 31.9342 4.91872 31.9556 4.95331 31.9701C4.9879 31.9847 5.02505 31.9922 5.06259 31.9922H7.17196C7.32665 31.9922 7.4497 31.8691 7.45321 31.718C7.52353 29.0039 8.61337 26.4621 10.5399 24.5355C12.5333 22.5422 15.1806 21.4453 18.0001 21.4453C20.8196 21.4453 23.4669 22.5422 25.4602 24.5355C27.3868 26.4621 28.4767 29.0039 28.547 31.718C28.5505 31.8727 28.6735 31.9922 28.8282 31.9922H30.9376C30.9751 31.9922 31.0123 31.9847 31.0469 31.9701C31.0815 31.9556 31.1128 31.9342 31.139 31.9073C31.1652 31.8805 31.1858 31.8486 31.1995 31.8137C31.2132 31.7788 31.2198 31.7414 31.2188 31.7039C31.1837 30.0234 30.8356 28.3887 30.1817 26.8453ZM18.0001 18.7734C16.3864 18.7734 14.8677 18.1441 13.7251 17.0016C12.5825 15.859 11.9532 14.3402 11.9532 12.7266C11.9532 11.1129 12.5825 9.59414 13.7251 8.45156C14.8677 7.30898 16.3864 6.67969 18.0001 6.67969C19.6138 6.67969 21.1325 7.30898 22.2751 8.45156C23.4177 9.59414 24.047 11.1129 24.047 12.7266C24.047 14.3402 23.4177 15.859 22.2751 17.0016C21.1325 18.1441 19.6138 18.7734 18.0001 18.7734Z" fill="white"/>
                        </svg>
                        </div>`;
    }
    divTag.innerHTML = `
      <div class="w-1/3 flex flex-col justify-center items-center mr-10">      
        ${html_picture}
        <h3 class="text-md font-medium mt-3">${fullName}</h3>
      </div>
      <div class="w-2/3">
        <div class="flex flex-row" id="review-stars-${id}" data-stars-total="${stars}">
          ${getStars(Number(stars))}
          <h3 class="ml-4 text-md font-medium" id="review-title-${id}">${title}</h3>
        </div>
        <span class="block">Posted on ${getDateTimeFormatted(date)}</span>
        <p class="mt-4" id="review-comments-${id}">${review}</p>
      </div>
      <button type="button" id="change-review" data-review-id="${id}">Change</button>`; // TODO: UPDATE CHANGE BUTTON AFTER STYLE UPDATING
    return divTag;
}

function getUpdateReviewForm(id, title, stars, review) {
    let divTag = document.createElement("div");
    divTag.setAttribute("class", "w-9/12 mt-5");
    divTag.setAttribute("id", "update-review")
    // Returns a form to update a review with and with all the old information in it.
    divTag.innerHTML = `
          <form method="post" class="flex flex-col" id="new-review-form">
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
              <label for="{{ form.review.id_for_label }}"
                     class="block text-gray-700 text-base mb-1">Review</label>
              <textarea name="review" cols="40" rows="5"
                        class="border border-customGray rounded py-4 px-4 shadow-inner w-full placeholder-gray-300 focus:outline-none"
                        maxlength="500" required="" id="id_review">${review}</textarea>
            </div>
            <div class="flex justify-between mb-3">
              <button id="review-update-cancel" class="text-center text-base text-customViolet rounded border border-customViolet py-1 px-4 focus:outline-none hover:shadow-md"
                      type="button" data-review-id="${id}">Cancel
              </button>
              <button class="bg-customBlue hover:shadow-md rounded text-customViolet text-base w-36 py-1 px-4 focus:outline-none"
                      type="submit">Update review
              </button>
            </div>
          </form>`;
    return divTag
}

function getStars(totalStars) {
    // Returns stars and with the correct stars filled and unfilled
    let stars = ""
    for (let i = 1; i <= 5; i++) {
        if (i <= totalStars) {
            stars += getFilledStar(i);
        } else {
            stars += getUnfilledStar(i);
        }
    }
    return stars;
}

function getFormStars(totalStars) {
    // Returns stars and with the correct stars hidden
    // based on the total stars parameter for a form.
    let stars = ""
    for (let i = 1; i <= 5; i++) {
        stars += `<button type="button" value="${i}" class="star-btn focus:outline-none">`;
        if (i === 1) {
            stars += getFilledStar(i)
        } else {
            if (i <= totalStars) {
                stars += getUnfilledStar(i, true);
                stars += getFilledStar(i);
            } else {
                stars += getUnfilledStar(i);
                stars += getFilledStar(i, true);
            }
        }
        stars += "</button>";
    }
    return stars;
}

function getFilledStar(id, hidden = false) {
    // Returns a filled star either with the correct id and hidden or not.
    hidden = hidden ? "hidden" : "";
    return `<svg id="star-filled-${id}" class="${hidden}" width="22" height="21" viewBox="0 0 22 21" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M11.2204 4.06848L12.7268 7.86637L13.0694 8.73021L13.9955 8.80806L18.0654 9.15022L14.9115 11.9833L14.2557 12.5723L14.4512 13.4319L15.3914 17.5652L12.0295 15.4119L11.2204 14.8937L10.4114 15.4119L7.04945 17.5652L7.98967 13.4319L8.1852 12.5723L7.52942 11.9833L4.37555 9.15022L8.44542 8.80806L9.37146 8.73021L9.71409 7.86637L11.2204 4.06848Z" fill="#F1C644" stroke="#F1C644" stroke-width="3"/>
            </svg>`;
}

function getUnfilledStar(id, hidden = false) {
    // Returns a unfilled star either with the correct id and hidden or not.
    hidden = hidden ? "hidden" : "";
    return `<svg id="star-unfilled-${id}" class="${hidden}" width="22" height="21" viewBox="0 0 22 21" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M11.0344 0L13.9351 7.31334L21.4642 7.9463L15.7278 13.0992L17.4804 20.8037L11.0344 16.675L4.58844 20.8037L6.341 13.0992L0.604612 7.9463L8.13373 7.31334L11.0344 0Z" fill="#D4D4D4"/>
            </svg>`;
}

function renderUpdateReviewForm(event) {
    // Puts the update form on screen with the data from the review pressed and then hides the review.
    let reviewId = event.currentTarget.dataset.reviewId;
    let title = document.getElementById(`review-title-${reviewId}`).innerText;
    let stars = document.getElementById(`review-stars-${reviewId}`).dataset.starsTotal
    let comments = document.getElementById(`review-comments-${reviewId}`).innerText;
    let review = document.getElementById(`review-${reviewId}`)
    let updateForm = getUpdateReviewForm(reviewId, title, stars, comments);
    review.classList.add("hidden");
    review.parentNode.insertBefore(updateForm, review);
    addSubmitListener("update-review", submitUpdateReview);
    addClickListener("review-update-cancel", cancelUpdateReview);
    addListenersToStars();
}

function cancelUpdateReview(event) {
    let reviewId = event.currentTarget.dataset.reviewId;
    document.getElementById("update-review").remove();
    document.getElementById(`review-${reviewId}`).classList.remove("hidden");
}

// Adds a click listener if the change review button is found.
addClickListener("change-review", renderUpdateReviewForm);

function addClickListener(elementId, callback) {
    // Adds a click listener if the element exists
    let element = document.getElementById(elementId);
    if (element) {
        element.addEventListener("click", callback);
    }
}

// TODO: Delete review button

function getDateTimeFormatted(datetime) {
    // Formats date time to the same format that the django backend uses.
    let date = new Date(datetime);
    let formatted = date.toLocaleString("en-US", { month: "short", day: "numeric", year: "numeric", hour: "numeric", minute: "numeric", hour12: true});
    return formatted.replace("AM", "a.m.").replace("PM", "p.m.");
}