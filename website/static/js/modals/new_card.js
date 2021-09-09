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
        let userInput = document.getElementById("userInput");
        let text = document.createTextNode(userInput.value);

        checkbox.type = 'checkbox';
        checkbox.name = 'interest';

        label.appendChild(checkbox);
        label.appendChild(text);

        let br = document.createElement('br');

        let container = document.getElementById('container');
        container.appendChild(label);
        container.appendChild(br);

        userInput.value = '';
    }
}

function toggleTag(id_element) {
    let el = document.getElementById(id_element);
    let classes = {
        "frontend": "success",
        "backend": "warning",
        "feature": "info",
        "bug": "danger",
        "addOne": "light",
    }

    Object.entries(classes).forEach(([k, v]) => {
        if (id_element === k) {
            el.classList.toggle("btn-"+v);
            el.classList.toggle("btn-outline-"+v);
        }
    })
}




