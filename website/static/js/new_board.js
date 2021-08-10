function ok_newBoard() {
    let name = document.getElementById("boardName").value;
    let category = document.getElementById("selectCategory").value;
    let favorite = document.getElementById("favoriteCheck").checked;

    make_modal_request([name,category,favorite], new_board_url, 'list')
    closeModal("newBoardModal")
}
