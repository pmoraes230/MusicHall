document.getElementById("searchText").addEventListener("input", function() {
    let searchText = this.value.toLowerCase();
    let cards = document.querySelectorAll(".card_ticket");

    cards.forEach(card => {
        let name = card.getAttribute("data-name");
        let cpf = card.getAttribute("data-cpf");

        if(name.includes(searchText) || cpf.includes(searchText)) {
            card.style.display = 'block'
        } else {
            card.style.display = 'none'
        }
    })
})