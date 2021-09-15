var list_to_delete = ""

addOnShowListener("deleteListModal", event => {
    let button = event.relatedTarget
    list_to_delete = button.getAttribute("data-bs-list")
    console.log(list_to_delete)

    let modal = document.getElementById("deleteListModal")
    let label = modal.getElementsByTagName("label").item(0)
    // si imposta il testo della label
    label.innerText = "Sei sicuro di voler eliminare la lista '" + list_to_delete + "'?"
})

function ok_deleteList() {
    //TODO: temporaneo ovviamente
    console.log("Eliminata lista " + list_to_delete)

    make_modal_request({"list_title": list_to_delete}, delete_list_url, 'deleteListModal', (data) => {
        insert_html(del_board_things_url, data)
    })

    closeModal("deleteListModal")
}