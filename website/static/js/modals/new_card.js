var target_list = ""

addOnShowListener("cardModal", e => {
    let button = e.relatedTarget
    target_list = button.getAttribute("data-bs-list")
})

function ok_newCard() {
    let name = document.getElementById("cardName").value;
    let description = document.getElementById("cardDescription").value;
    let list = document.getElementById(target_list);
    let template = document.getElementById('cardTemplate');

    let data = {
        "target_type": "card",
        "target_id": {
            "target_id_board": targetBoard,
            "target_id_list": target_list.replace("list_", "")
        },
        "new_data": {
            "card_name": name,
            "card_descr": description
        }
    }

    make_modal_request(data, new_card_url, "cardModal", (data) => {
        list.insertAdjacentHTML("beforeend", data)
    })
}

// grazie stackoverlow
function truncate(str, n) {
    return (str.length > n) ? str.substr(0, n - 1) + '...' : str;
};