function ok_newBoard() {

    let name = document.getElementById("boardName").value;
    let category = document.getElementById("selectCategory").value;
    let favorite = document.getElementById("favoriteCheck").checked;
    console.log(name, category, favorite);



    let ul = document.getElementById("list");
    let li = document.createElement("li");
    li.className = "list-group-item fs-5"
    li.innerText=name;
    ul.appendChild(li);

    closeModal("newBoardModal")
}
