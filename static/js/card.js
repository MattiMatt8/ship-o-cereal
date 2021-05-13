function fixCardFormatting(e) {
    // Formats card to a maximum of 16 digits and
    // puts - between every four numbers.
    let new_str = "";
    let numbers = 0;
    for(let i = 0; i<e.target.value.length; i++) {
        if (i === 19) {
            break;
        }
        if (e.target.value[i] === "-") {
            continue;
        }
        numbers++;
        new_str += e.target.value[i];
        if ((numbers % 4) === 0 && i !== 18) {
            new_str += "-";
        }
    }
    e.target.value = new_str;
}

document.getElementById("id_number").addEventListener("keyup", fixCardFormatting);
