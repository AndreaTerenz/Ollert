function ok_newBoard() {
    let data = {
        name : document.getElementById("boardName").value,
        category : document.getElementById("selectCategory").value,
        favorite : document.getElementById("favoriteCheck").checked
    }

    make_modal_request(data, new_board_url, "list", "newBoardModal")
}
