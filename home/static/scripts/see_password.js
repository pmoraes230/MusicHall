const inputPassword = document.getElementById("password");
const btnEye = document.getElementById("btn_password");
const eye = document.getElementById("eye");

btnEye.addEventListener("click", function() {
    if(inputPassword.type == "password") {
        inputPassword.type = "text"
        eye.src = "/static/icons/EyeSlash.svg"
    } else {
        inputPassword.type = "password"
        eye.src = "/static/icons/Eye.svg"
    }
})