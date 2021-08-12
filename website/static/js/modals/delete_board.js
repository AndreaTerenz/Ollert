var board = ""

addOnShowListener("#deleteModal", event => {
    // con questo barbatrucco si ottiene il pulsante che ha triggerato l'evento
    let button = event.relatedTarget
    // il pulsante contiene un attributo custom ('data-bs-board') che ha come valore il nome della board a cui è legato
    // tale valore viene assegnato a una variabile globale
    board = button.getAttribute("data-bs-board")

    // La domanda da "personalizzare" è in una label all'interno del modale, che viene selezionata
    let label = modal.getElementsByTagName("label").item(0)
    // si imposta il testo della label
    label.innerText = "Sei sicuro di voler eliminare la board '" + board + "'?"
})

function ok_delete() {
    //TODO: temporaneo ovviamente
    console.log("Eliminata board " + board)

    closeModal("deleteModal")
}