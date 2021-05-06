const MAIN_URL = "/cart2";

// Function getCookie from: https://docs.djangoproject.com/en/3.0/ref/csrf/#ajax
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const CSRF_TOKEN = getCookie('csrftoken');

function addToCart(id) {
    axios.post(`${MAIN_URL}/add/${id}/`, {'content': {'quantity': 4, 'override_quantity': false}}, { headers: {"X-CSRFToken": CSRF_TOKEN }})
        .then((response) => {
            console.log(response.data)
        })
        .catch((error) => {
            console.log(error);
        });
}

addToCart(5);