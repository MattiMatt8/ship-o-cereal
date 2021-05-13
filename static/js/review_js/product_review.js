// -- Review star functionality --
let starInput;
let stopHoverMove;

function getDateTimeFormatted(datetime) {
    // Formats date time to the same format that the django backend uses.
    let date = new Date(datetime);
    let formatted = date.toLocaleString("en-US", {
        month: "short",
        day: "numeric",
        year: "numeric",
        hour: "numeric",
        minute: "numeric",
        hour12: true
    });
    return formatted.replace("AM", "a.m.").replace("PM", "p.m.");
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
        stars += `<button type="button" value = "${i}" class="star-btn focus:outline-none">`;
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
};

function getFilledStar(id, hidden = false) {
    // Returns a filled star either with the correct id and hidden or not.
    hidden = hidden ? "hidden" : "";
    return `<svg id="star-filled-${id}" class="${hidden}"
    width="22" height="21" viewBox="0 0 22 21" fill="none" xmlns="http://www.w3.org/2000/svg" >
    <path d = "M11.2204 4.06848L12.7268 7.86637L13.0694 8.73021L13.9955 8.80806L18.0654 9.15022L14.9115 11.9833L14.2557 12.5723L14.4512 13.4319L15.3914 17.5652L12.0295 15.4119L11.2204 14.8937L10.4114 15.4119L7.04945 17.5652L7.98967 13.4319L8.1852 12.5723L7.52942 11.9833L4.37555 9.15022L8.44542 8.80806L9.37146 8.73021L9.71409 7.86637L11.2204 4.06848Z"
    fill="#F1C644" stroke="#F1C644" stroke-width="3"/></svg>`;
};

function getUnfilledStar(id, hidden = false) {
    // Returns a unfilled star either with the correct id and hidden or not.
    hidden = hidden ? "hidden" : "";
    return `<svg id="star-unfilled-${id}" class="${hidden}" width="22" height="21" viewBox="0 0 22 21" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M11.0344 0L13.9351 7.31334L21.4642 7.9463L15.7278 13.0992L17.4804 20.8037L11.0344 16.675L4.58844 20.8037L6.341 13.0992L0.604612 7.9463L8.13373 7.31334L11.0344 0Z" fill="#D4D4D4"/>
            </svg>`;
};

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
};

function starHover(event) {
    // When hovered over it calls the function change stars
    // unless a star has been pressed on then it does nothing
    if (stopHoverMove) return;
    changeStars(event.currentTarget.value);
};

function starPress(event) {
    // When a stared is pressed it either changes it so they stop changing
    // when being hovered over but only when pressed on.
    if (stopHoverMove) {
        changeStars(event.currentTarget.value);
    }
    stopHoverMove = true;
};

function addListenersToStars() {
    // Adds listeners to the review stars so they function properly when hovered over.
    let starButtons = document.getElementsByClassName("star-btn");
    starInput = document.getElementById("id_stars");
    stopHoverMove = false;
    for (let starButton of starButtons) {
        starButton.addEventListener("mouseover", starHover);
        starButton.addEventListener("click", starPress);
    }
};

// Review add, update & delete requests
function addSubmitListener(elementId, callback) {
    // Adds a submit listener if the element exists
    let element = document.getElementById(elementId);
    if (element) {
        element.addEventListener("submit", callback);
    }
};

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
};

function deleteReview(callback) {
    // Calls the server to delete a review and if
    // it is successful it calls the render delete review function.
    axios
        .post(
            "reviews/delete/",
            null,
            {headers: {"X-CSRFToken": CSRF_TOKEN}}
        )
        .then((response) => {
            console.log("what")
            renderDeleteReview(response.data.data.id);
        })
        .catch((error) => {
            console.log(error);
        });
};

function addClickListener(elementId, callback) {
    // Adds a click listener if the element exists
    let element = document.getElementById(elementId);
    if (element) {
        element.addEventListener("click", callback);
    }
};

// If there is a new review form this will add the stars to it
addListenersToStars();
// Event listener for the submit of a new review
addSubmitListener("new-review-form", submitNewReview);
// Adds a click listener if the change review button is found.
addClickListener("change-review", renderUpdateReviewForm);
// Adds a click listener if the delete review button is found.
addClickListener("delete-review", deleteReview);