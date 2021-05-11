const starButtons = document.getElementsByClassName("star-btn");
const starInput = document.getElementById("id_stars");
let stopHoverMove = false;

for (let starButton of starButtons) {
    starButton.addEventListener("mouseover", starHover);
    starButton.addEventListener("click", starPress);
}

function changeStars(starNum) {
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
    if (stopHoverMove) return;
    changeStars(event.currentTarget.value);
}

function starPress(event) {
    if (stopHoverMove) {
        changeStars(event.currentTarget.value);
    }
    stopHoverMove = true;
}