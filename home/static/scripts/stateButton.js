const campInput = document.getElementById("ticket_input");
const btnValidation = document.getElementById("btnValidation");

function stateButton() {
    if (campInput.value.trim() !== '') {
        btnValidation.removeAttribute("disabled");
    } else {
        btnValidation.setAttribute("disabled", "true")
    }
}

stateButton()

campInput.addEventListener('input', stateButton)