var list_id = ""

addOnShowListener("deleteListModal", event => {
    let button = event.relatedTarget
    list_id = button.getAttribute("data-bs-list")
    let title = button.getAttribute("data-bs-list-title")
    console.log(list_id)

    let modal = document.getElementById("deleteListModal")
    let label = modal.getElementsByTagName("label").item(0)
    // si imposta il testo della label
    label.innerText = "Sei sicuro di voler eliminare la lista '" + title + "'?"
})

function ok_deleteList() {
    //TODO: temporaneo ovviamente
    console.log("Eliminata lista " + list_id)

    let id = parseInt(list_id.replace("list_", ""))

    let data = {
        "board": currentBoard,
        "targets": [{
            "target_type": "list",
            "target_id": {
                "target_id_list": id
            }
        }]
    }

    make_modal_request(data, delete_list_url, 'deleteListModal', (data) => {
        insert_html(main_row_id, data)
    })
}