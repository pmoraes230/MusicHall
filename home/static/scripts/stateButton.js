const campInput = document.getElementById("ticket_input");
const btnValidation = document.getElementById("btnValidation");

if (campInput.value.trim() !== ' ') {
    btnValidation.removeAttribute("disabled");
} else {
    btnValidation.setAttribute("disabled", "true")
}