function toggleLists() {
    let isChecked = document.getElementById("flexSwitchCheckDefault").checked;
    let board_list = document.getElementById(boards_list_id);
    let shared_board = document.getElementById(shared_boards)
    let category_list = document.getElementById(categories_list_id)

    if (isChecked) {
        board_list.style.display="none";
        shared_board.style.display="none";
        category_list.style.display="block";
    }
    else {
        category_list.style.display="none";
        board_list.style.display="block";
        shared_board.style.display="block";
    }
}