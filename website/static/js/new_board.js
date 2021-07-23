function ok_newBoard() {
    let name = document.getElementById("boardName").value;
    let category = document.getElementById("selectCategory").value;
    let favorite = document.getElementById("favoriteCheck").checked;

    console.log(name, category, favorite);

    let url = new_board_url.replace("$1", name).replace("$2", category).replace("$3", favorite)

    fetch(url, {
        method: "POST",
        credentials: 'same-origin',
        headers: {
            "X-CSRFToken": Cookies.get('csrftoken'),
            "X-Requested-With": "XMLHttpRequest"
        },
    }).then((r) => {
        console.log(r.status)
        let ul = document.getElementById("list");
        let li = document.createElement("li");
        li.className = "list-group-item fs-5"
        li.innerText = name;
        ul.appendChild(li);

        closeModal("newBoardModal")
    })
}
