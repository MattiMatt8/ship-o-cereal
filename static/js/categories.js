const filterBtn = document.getElementsByClassName("filter-btn");

function submitForm(event) {
    // Submits the form the item clicked is in.
    event.target.form.submit();
}

for (let btn of filterBtn) {
    // Adds event listeners to buttons that are in the filter form
    // so we can submit the form automatically when it changes.
    btn.addEventListener("change", submitForm);
}
