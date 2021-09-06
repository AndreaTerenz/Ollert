var card_data = ""

addOnShowListener("cardModal", e => {
    let button = e.relatedTarget
    let card_data_id = button.getAttribute("data-bs-card-json")

    card_data = JSON.parse(document.getElementById(card_data_id).textContent);

    document.getElementById("cardModalTItle").innerText = card_data.card_title

    let description = document.getElementById("cardModalDescr")

    if (card_data.card_descr !== "") {
        document.getElementById("cardModalDescr").innerText = card_data.card_descr
        description.classList.remove("text-muted")
    } else {
        document.getElementById("cardModalDescr").innerText = "Nessuna descrizione"
        description.classList.add("text-muted")
    }
})

function ok_viewCard() {
    closeModal("cardModal")
}