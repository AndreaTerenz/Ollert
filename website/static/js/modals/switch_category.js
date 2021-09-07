function toggleLists() {
    let isChecked = document.getElementById("flexSwitchCheckDefault").checked;
    let board_list = document.getElementById(boards_list_id);
    let category_list = document.getElementById(categories_list_id)

    if (isChecked) {
        board_list.style.display="none";
        category_list.style.display="block";
    }
    else {
        category_list.style.display="none";
        board_list.style.display="block";
    }
}