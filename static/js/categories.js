// function submitBrandFilter(e) {
//     e.target.form.submit();
// }
//
// function submitLabelFilter(e) {
//
// }

function submitFilter(e) {
    e.target.form.submit();
}

document.getElementById("id_brand").addEventListener("change", submitFilter);
document.getElementById("id_labels").addEventListener("change", submitFilter);
document.getElementById("id_ordering").addEventListener("change", submitFilter);
