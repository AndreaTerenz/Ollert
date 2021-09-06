var board_to_delete = ""

addOnShowListener("deleteModal", event => {
    // con questo barbatrucco si ottiene il pulsante che ha triggerato l'evento
    let button = event.relatedTarget
    // il pulsante contiene un attributo custom ('data-bs-board') che ha come valore il nome della board a cui è legato
    // tale valore viene assegnato a una variabile globale
    board_to_delete = button.getAttribute("data-bs-board")

    // La domanda da "personalizzare" è in una label all'interno del modale, che viene selezionata
    let modal = document.getElementById("deleteModal")
    let label = modal.getElementsByTagName("label").item(0)
    // si imposta il testo della label
    label.innerText = "Sei sicuro di voler eliminare la board '" + board_to_delete + "'?"
})

function ok_delete() {
    //TODO: temporaneo ovviamente
    console.log("Eliminata board " + board_to_delete)

    make_modal_request({name: board_to_delete}, delete_board_url, 'deleteModal', (data) => {
        insert_html('list', data)
    })
}