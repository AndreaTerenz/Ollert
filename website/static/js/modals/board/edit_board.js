var edit_modal
var initial_data

addOnShowListener("editBoardModal", event => {
    let button = event.relatedTarget
    let board_to_edit = button.getAttribute("data-bs-board")
    initial_data = JSON.parse(document.getElementById(board_to_edit + '_json').textContent);

    edit_modal = document.getElementById("editBoardModal")
    edit_modal.querySelector("#boardName").value = initial_data.name
    edit_modal.querySelector("#boardDescription").value = (initial_data.description) ? initial_data.description : ""
    edit_modal.querySelector("#selectCategory").value = (initial_data.category) ? initial_data.category : "NaN"
    edit_modal.querySelector("#favoriteCheck").checked = initial_data.favorite
})

function ok_editBoard() {
    let edits = []
    let request_data = {
        "board_name": initial_data.name,
        "edits": []
    }

    let name = edit_modal.querySelector("#boardName").value
    let description = edit_modal.querySelector("#boardDescription").value
    let category = edit_modal.querySelector("#selectCategory").value
    let favorite = edit_modal.querySelector("#favoriteCheck").checked

    if (initial_data.name !== name) {
        edits.push({
            "target_field": "name",
            "new_value": name
        })
    }

    if (initial_data.description !== description) {
        edits.push({
            "target_field": "description",
            "new_value": description
        })
    }

    if (initial_data.category !== category) {
        edits.push({
            "target_field": "category",
            "new_value": category
        })
    }

    if (initial_data.favorite !== favorite) {
        edits.push({
            "target_field": "favorite",
            "new_value": favorite
        })
    }

    request_data["edits"] = edits

    make_modal_request(request_data, edit_board_url, "editBoardModal", (data) => {
        insert_html('board-list', data)
    })

    closeModal("editBoardModal")
}