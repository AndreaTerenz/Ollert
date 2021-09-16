var card_data = ""

addOnShowListener("cardModal", e => {
    let button = e.relatedTarget
    let card_data_id = button.getAttribute("data-bs-card-json")

    card_data = JSON.parse(document.getElementById(card_data_id).textContent);

    document.getElementById("cardModalTItle").innerText = card_data.card_title

    set_card_field("cardModalDescr", card_data.card_descr, "Nessuna descrizione")
    set_card_field("cardModalDate", card_data.card_date, "Nessuna data")
    set_checklist_field()
    set_member_field()
})

function set_card_field(el_id, value, no_value_text) {
    let element = document.getElementById(el_id)

    if (value) {
        element.innerText = value
        element.classList.remove("text-muted")
    } else {
        element.innerText = no_value_text
        element.classList.add("text-muted")
    }
}

function set_checklist_field() {
    let container = document.getElementById('cardModalCheck')
    container.innerText = ""

    for (const check in card_data.card_checks) {
        let checkbox = document.createElement('input');
        let label = document.createElement('label')
        let checkText = document.createTextNode(check);

        checkbox.type = 'checkbox';
        checkbox.checked = card_data.card_checks[check]

        label.appendChild(checkbox);
        label.appendChild(checkText);
        label.classList.add("mb-2")

        container.appendChild(label)
        container.classList.remove("text-muted")
    }

    if (isEmpty(card_data.card_checks)) {
        container.innerText = "Nessuna checkist"
        container.classList.add("text-muted")
    }

}

function set_member_field() {
    let parent = document.getElementById('cardModalMember')
    if (card_data.card_members) {
        parent.innerText = card_data.card_members
        parent.classList.remove("text-muted")
    }

    if (isEmpty(card_data.card_members)) {
        parent.innerText = "Nessun membro assegnato"
        parent.classList.add("text-muted")
    }
}

function ok_viewCard() {
    closeModal("cardModal")
}

function isEmpty(obj) {
    return Object.keys(obj).length === 0;
}
