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
        if (r.status === 200) {
            return r.text()
        }
        return null
    }).then((data) => {
        if (data) {
            let ul = document.getElementById("list")
            ul.innerHTML = data
        }
        closeModal("newBoardModal")
    })
}
