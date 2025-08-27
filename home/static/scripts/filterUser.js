document.getElementById("searchUser").addEventListener("input", function() {
    let searchText = this.value.toLowerCase();
    let cards = document.querySelectorAll(".card_user")

    cards.forEach(card => {
        let name = card.getAttribute("data-name")
        let email = card.getAttribute("data-email")

        if(name.includes(searchText) || email.includes(searchText)) {
            card.style.display = "block"
        } else {
            card.style.display = "none"
        }
        
    })
})