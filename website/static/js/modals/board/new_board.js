function ok_newBoard() {
    let modal = document.getElementById("newBoardModal")
    let data = {
        name : modal.querySelector("#boardName").value,
        category : modal.querySelector("#selectCategory").value,
        description: modal.querySelector("#boardDescription").value,
        favorite : modal.querySelector("#favoriteCheck").checked
    }

    make_modal_request(data, new_board_url, "newBoardModal", (data) => {
        insert_html(boards_list_id, data)
    })
}
