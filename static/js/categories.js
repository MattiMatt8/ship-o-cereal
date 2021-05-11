const filterBtn = document.getElementsByClassName("filter-btn");

function submitForm(event) {
    event.target.form.submit();
}

for (let btn of filterBtn) {
    btn.addEventListener("change", submitForm);
}
