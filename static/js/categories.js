function submitBrandFilter(e) {
    e.target.form.submit();
}

document.getElementById("id_brand").addEventListener("change", submitBrandFilter);
