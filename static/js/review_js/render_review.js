function newReviewContainer (id) {
    // Create a new div & set the attributes
    let reviewContainer = document.createElement("div");
    reviewContainer.setAttribute("class", "flex flex-col my-8 items-center md:flex-row md:items-start md:justify-start");
    reviewContainer.setAttribute("id", `review-${id}`);

    return reviewContainer;
};

function newProfileContainer (picture, fullName) {
    let HtmlPicture;

    // Parent container for profile info
    let profileContainer = document.createElement("div");

    // Child container for image & full name of user
    let imageContainer = document.createElement("div");

    // Child container for full name
    let nameContainer = document.createElement("div");
    let nameTag = document.createElement("h3");
    nameTag.innerText = fullName;

    profileContainer.setAttribute("class", "w-32 md:mr-8");
    imageContainer.setAttribute("class", "flex flex-col justify-center items-center w-32");
    nameContainer.setAttribute("class", "flex justify-center text-center");
    nameTag.setAttribute("class", "text-md font-medium mt-3");

    // If user has a profile picture
    if (picture) {
        HtmlPicture = `<img className="w-16 h-16 rounded-full object-cover object-center" src="${picture}">`;
    // If user does not have a profile picture, add the default icon
    } else {
        HtmlPicture = `<div class="bg-customGray rounded-full w-16 h-16 flex justify-center items-center">
                         <svg class="w-7 h-7 lg:w-8 lg:h-8" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
                           <path d="M30.1817 26.8453C29.5185 25.2744 28.5561 23.8475 27.3481 22.6441C26.1438 21.4373 24.7171 20.475 23.147 19.8105C23.1329 19.8035 23.1188 19.8 23.1048 19.793C25.295 18.2109 26.7188 15.634 26.7188 12.7266C26.7188 7.91016 22.8165 4.00781 18.0001 4.00781C13.1837 4.00781 9.28134 7.91016 9.28134 12.7266C9.28134 15.634 10.7052 18.2109 12.8954 19.7965C12.8813 19.8035 12.8673 19.807 12.8532 19.8141C11.2782 20.4785 9.86493 21.4312 8.65204 22.6477C7.44516 23.852 6.48292 25.2786 5.81845 26.8488C5.16567 28.386 4.81362 30.0341 4.78134 31.7039C4.7804 31.7414 4.78698 31.7788 4.80069 31.8137C4.81441 31.8486 4.83498 31.8805 4.86119 31.9073C4.8874 31.9342 4.91872 31.9556 4.95331 31.9701C4.9879 31.9847 5.02505 31.9922 5.06259 31.9922H7.17196C7.32665 31.9922 7.4497 31.8691 7.45321 31.718C7.52353 29.0039 8.61337 26.4621 10.5399 24.5355C12.5333 22.5422 15.1806 21.4453 18.0001 21.4453C20.8196 21.4453 23.4669 22.5422 25.4602 24.5355C27.3868 26.4621 28.4767 29.0039 28.547 31.718C28.5505 31.8727 28.6735 31.9922 28.8282 31.9922H30.9376C30.9751 31.9922 31.0123 31.9847 31.0469 31.9701C31.0815 31.9556 31.1128 31.9342 31.139 31.9073C31.1652 31.8805 31.1858 31.8486 31.1995 31.8137C31.2132 31.7788 31.2198 31.7414 31.2188 31.7039C31.1837 30.0234 30.8356 28.3887 30.1817 26.8453ZM18.0001 18.7734C16.3864 18.7734 14.8677 18.1441 13.7251 17.0016C12.5825 15.859 11.9532 14.3402 11.9532 12.7266C11.9532 11.1129 12.5825 9.59414 13.7251 8.45156C14.8677 7.30898 16.3864 6.67969 18.0001 6.67969C19.6138 6.67969 21.1325 7.30898 22.2751 8.45156C23.4177 9.59414 24.047 11.1129 24.047 12.7266C24.047 14.3402 23.4177 15.859 22.2751 17.0016C21.1325 18.1441 19.6138 18.7734 18.0001 18.7734Z" fill="white"/>
                         </svg>
                       </div>`;
    }

    imageContainer.innerHTML = HtmlPicture;
    profileContainer.appendChild(imageContainer);
    imageContainer.appendChild(nameContainer);
    nameContainer.appendChild(nameTag);

    return profileContainer;
};

function newReviewContentContainer(id, title, stars, review, date) {
    let reviewContentContainer = document.createElement("div");

    // Fill container with review contents, stars and buttons
    reviewContentContainer.setAttribute("class", "flex flex-col");
    reviewContentContainer.innerHTML = `
              <div>
               <div class="flex flex-col md:flex-row md:items-center" id="review-stars-${id}" data-stars-total="${stars}">
                  <div class="flex flex-row justify-center my-2 md:justify-start">
                    ${getStars(Number(stars))}
                  </div>
                  <div class="flex flex-row justify-center md:justify-start">
                    <h3 class="ml-4 text-md font-medium" id="review-title-${id}">${title}</h3>
                  </div>
               </div>
               <span class="block text-center md:text-left">Posted on ${getDateTimeFormatted(date)}</span>
               <p class="mt-2 text-center italic md:text-left md:mt-4" id="review-comments-${id}">${review}</p>
              </div>
              <div class="flex flex-row justify-center mt-4 md:justify-start">
                  <button class="text-customRed focus:outline-none border-b-2 border-customRed border-opacity-0 hover:border-opacity-75 mx-4 md:ml-0"
                          type="button" id="delete-review" data-review-id="${id}">Delete
                  </button>
                  <button class="focus:outline-none border-b-2 border-customViolet border-opacity-0 hover:border-opacity-75 mx-4"
                          type="button" id="change-review" data-review-id="${id}">Change
                  </button>
              </div>`

    return reviewContentContainer;
};

function getReviewFilled(id, title, stars, review, picture, date, fullName) {

    // Returns a review formatted with everything filled out and ready.
    let reviewContainer = newReviewContainer(id);
    let profileContainer = newProfileContainer(picture, fullName);
    let reviewContents = newReviewContentContainer(id, title, stars, review, date);


    reviewContainer.appendChild(profileContainer);
    reviewContainer.appendChild(reviewContents);

    console.log(reviewContainer);
    return reviewContainer;
};

function renderNewReview(data) {
    // Renders the new review for the user and removes the form it was submitted in.
    let newReview = getReviewFilled(data.id, data.title, data.stars, data.review, data.profile_image, data.date, data.full_name);

    let reviewsHeader = document.getElementById("reviews-header");
    document.getElementById("new-review").remove();

    reviewsHeader.parentNode.insertBefore(newReview, reviewsHeader.nextSibling);
    addClickListener("change-review", renderUpdateReviewForm);
    addClickListener("delete-review", deleteReview);

    if (reviewsHeader.innerText === "No reviews yet.") reviewsHeader.innerText = "Reviews";
};

function submitNewReview(event) {
    submitReview(event, "new", renderNewReview);
};

function renderUpdateOldReview(data) {
    // Updates the old form in the browser with the new data received from the server
    // and hides the update form.
    let review = document.getElementById(`review-${data.id}`);
    let reviewElements = document.getElementById(`review-stars-${data.id}`).parentNode;
    reviewElements.innerHTML = `
    <div class="flex flex-row" id="review-stars-${data.id}" data-stars-total="${data.stars}">
        ${getStars(data.stars)}
        <h3 class="ml-4 text-md font-medium" id="review-title-${data.id}">${data.title}</h3>
      </div>
      <span class="block">Posted on ${getDateTimeFormatted(data.date)}</span>
      <p class="mt-4" id="review-comments-${data.id}">${data.review}</p>
    `;
    document.getElementById("update-review").remove();
    review.classList.remove("hidden");
};

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
};

function cancelUpdateReview(event) {
    // Removes the update form for a review from the screen
    // and unhides the review meant to be updated.

    let reviewId = event.currentTarget.dataset.reviewId;
    document.getElementById("update-review").remove();
    document.getElementById(`review-${reviewId}`).classList.remove("hidden");
};

function submitUpdateReview(event) {
    // Calls the submit axios function to update the review on the backend
    // and with the correct callback function to then render it in the browser.
    submitReview(event, "update", renderUpdateOldReview);
};

function renderDeleteReview(id) {
    // Deletes the review and renders a form to submit a new review.
    document.getElementById(`review-${id}`).remove();
    let newReviewForm = getNewReviewForm();
    let reviewsHeader = document.getElementById("reviews-header");

    if (reviewsHeader.parentNode.children.length === 1) reviewsHeader.innerText = "No reviews yet.";
    reviewsHeader.parentNode.insertBefore(newReviewForm, reviewsHeader.nextSibling);

    addListenersToStars();
    addSubmitListener("new-review-form", submitNewReview);
};