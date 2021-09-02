var card_data = ""

addOnShowListener("cardModal", e => {
    let button = e.relatedTarget
    card_data = button.getAttribute("data-bs-card-data")
    //EVERYONE TAKE A SEAT, WELCOME TO DJANGO CIRCUS
    card_data = card_data.replaceAll("'", "\"")
    card_data = JSON.parse(card_data)

    document.getElementById("cardModalTItle").innerText = card_data.card_title

    let card_descr = document.getElementById("cardModalDescr")

    if (card_data.card_descr !== "") {
        document.getElementById("cardModalDescr").innerText = card_data.card_descr
        card_descr.classList.remove("text-muted")
    }
    else {
        document.getElementById("cardModalDescr").innerText = "Nessuna descrizione"
        card_descr.classList.add("text-muted")
    }
})

function ok_viewCard() {
    closeModal("cardModal")
}