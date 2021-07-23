function ok_newCard() {
    let name = document.getElementById("cardName").value;
    let description = document.getElementById("cardDescription").value;
    let lista = document.getElementById('cardsList');
    let template = document.getElementById('cardTemplate');

    console.log(name, description);
    let clone = template.content.cloneNode(true);
    lista.appendChild(clone);

    closeModal("cardModal")
}
