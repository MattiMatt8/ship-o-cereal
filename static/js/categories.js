function submitBrandFilter(e) {
    e.target.form.submit();
}

function submitLabelFilter(e) {
    e.target.form.submit();
}

document.getElementById("id_brand").addEventListener("change", submitBrandFilter);
document.getElementById("id_labels").addEventListener("change", submitBrandFilter);
