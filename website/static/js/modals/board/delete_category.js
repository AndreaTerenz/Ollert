var category_to_delete = ""

addOnShowListener("deleteCategoryModal", event => {
    // con questo barbatrucco si ottiene il pulsante che ha triggerato l'evento
    let button = event.relatedTarget
    // il pulsante contiene un attributo custom ('data-bs-board') che ha come valore il nome della board a cui è legato
    // tale valore viene assegnato a una variabile globale
    category_to_delete = button.getAttribute("data-bs-board")

    // La domanda da "personalizzare" è in una label all'interno del modale, che viene selezionata
    let modal = document.getElementById("deleteCategoryModal")
    let label = modal.getElementsByTagName("label").item(0)
    // si imposta il testo della label
    label.innerText = "Sei sicuro di voler eliminare la categoria '" + category_to_delete + "'?"
})

function ok_deleteCategory() {
    //TODO: temporaneo ovviamente
    console.log("Eliminata categoria " + category_to_delete)

    make_modal_request({"cat_name": category_to_delete}, delete_category_url, 'deleteCategoryModal', (data) => {
        insert_html(categories_list_id, data)
    })

    closeModal("deleteCategoryModal")
}