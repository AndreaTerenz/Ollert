var target_list = ""

addOnShowListener("newCardModal", e => {
    let button = e.relatedTarget
    target_list = button.getAttribute("data-bs-list")
})

function ok_newCard() {
    let name = document.getElementById("cardName").value;

    if (name) {
        let description = document.getElementById("cardDescription").value;
        let list = document.getElementById(target_list);

        let data = {
            "target_type": "card",
            "target_id": {
                "target_id_board": currentBoard,
                "target_id_list": target_list.replace("list_", "")
            },
            "new_data": {
                "card_name": name,
                "card_descr": description
            }
        }

        make_modal_request(data, new_card_url, "newCardModal", (data) => {
            list.insertAdjacentHTML("beforeend", data)
        })
    }
}

// grazie stackoverlow
function truncate(str, n) {
    return (str.length > n) ? str.substr(0, n - 1) + '...' : str;
}

function toggleElement(id_element) {
    let elements = document.getElementById(id_element);
    let visibility = elements.style.display;

    if (visibility === 'none')
        elements.style.display = "block";
    else
        elements.style.display = "none";
}

function showChecklist() {
    document.getElementById('buttonChecklist').onclick = function () {
        let checkbox = document.createElement('input');
        let label = document.createElement('label')
        let userInput = document.getElementById("userInput").value;
        let text = document.createTextNode(userInput);

        checkbox.type = 'checkbox';
        checkbox.name = 'interest';

        label.appendChild(checkbox);
        label.appendChild(text);

        let br = document.createElement('br');

        let container = document.getElementById('container');
        container.appendChild(label);
        container.appendChild(br);
    }
}

function showLabels(id_element) {

    if(id_element === 'frontend')
        if (document.getElementById(id_element).className === "btn btn-outline-success")
            document.getElementById(id_element).className = "btn btn-success";
        else document.getElementById(id_element).className = "btn btn-outline-success";

    if (id_element === 'backend')
         if (document.getElementById(id_element).className === "btn btn-outline-warning")
            document.getElementById(id_element).className = "btn btn-warning";
        else document.getElementById(id_element).className = "btn btn-outline-warning";

    if (id_element === 'feature')
         if (document.getElementById(id_element).className === "btn btn-outline-info")
            document.getElementById(id_element).className = "btn btn-info";
        else document.getElementById(id_element).className = "btn btn-outline-info";

    if (id_element === 'bug')
         if (document.getElementById(id_element).className === "btn btn-outline-danger")
            document.getElementById(id_element).className = "btn btn-danger";
        else document.getElementById(id_element).className = "btn btn-outline-danger";

    if (id_element === 'addOne')
         if (document.getElementById(id_element).className === "btn btn-outline-light")
            document.getElementById(id_element).className = "btn btn-light";
        else document.getElementById(id_element).className = "btn btn-outline-light";

}




