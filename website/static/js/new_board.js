function ok_newBoard() {

    let name = document.getElementById("boardName").value;
    let category = document.getElementById("selectCategory").value;
    let favorite = document.getElementById("favoriteCheck").checked;
    console.log(name, category, favorite);

    console.log(Cookies.get('csrftoken'))
    fetch('http://localhost:8000/create_board/' + name + '/' + category + '/' + favorite, {
        mode: 'cors',
        method: "POST",
        credentials: 'same-origin',
        headers: {
            "X-CSRFToken": Cookies.get('csrftoken'),
        },

    }).then((r) => {
        console.log(r.status)
        let ul = document.getElementById("list");
        let li = document.createElement("li");
        console.log('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
        li.className = "list-group-item fs-5"
        li.innerText = name;
        ul.appendChild(li);

        closeModal("newBoardModal")
    })
}
