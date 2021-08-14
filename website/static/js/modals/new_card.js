function ok_newCard() {
    let name = document.getElementById("cardName").value;
    let description = document.getElementById("cardDescription").value;
    let lista = document.getElementById('cardsList');
    let template = document.getElementById('cardTemplate');

    console.log(name, description);
    let clone = template.content.cloneNode(true);
    clone.querySelector(".card-header").textContent = name
    clone.querySelector(".card-body").textContent = truncate(description, 64)
    lista.appendChild(clone);

    closeModal("cardModal")
}

// grazie stackoverlow
function truncate(str, n) {
    return (str.length > n) ? str.substr(0, n - 1) + '...' : str;
};