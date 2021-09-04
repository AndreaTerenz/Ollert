function getValue() {
    let isChecked = document.getElementById("flexSwitchCheckDefault").checked;
    let board_list = document.getElementById("board-list");
    let category_list = document.getElementById("category-list")


    if (isChecked) {
        board_list.style.display="none";
        category_list.style.display="block";
    }
    else {
        category_list.style.display="none";
        board_list.style.display="block";
    }
}