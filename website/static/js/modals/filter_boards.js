function filter_boards() {
    let preferiti = document.getElementById("preferiti").checked;
    let non_classificate = document.getElementById('non_classificate').checked;

    let category_checks = document.querySelectorAll()

    let board_list = document.getElementById(boards_list_id);

    if (preferiti) {
        for (const boardListKey in board_list) {
            if (board_name.favorite)
                board_name.style.display = "block";
            else board_name.style.display = "none";
        }
    }
}

/*


    board_list.style.display = "none";
    shared_board.style.display = "none";
    category_list.style.display = "block";


else
{
    category_list.style.display = "none";
    board_list.style.display = "block";
    shared_board.style.display = "block";
}
}*/
