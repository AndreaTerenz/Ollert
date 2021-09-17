var selected_cards = []

addOnShowListener("editCardModal", event => {

    // La domanda da "personalizzare" è in una label all'interno del modale, che viene selezionata
    let modal = document.getElementById("editCardModal")
    let label = modal.getElementsByTagName("label").item(0)
    // si imposta il testo della label
    if (selected_cards.length === 1) {
        label.innerText = "Sei sicuro di voler eliminare la card '" + selected_cards[0] + "'?"
    } else
        label.innerText = "Sei sicuro di voler eliminare " + selected_cards.length + " card ?"
})


function selectCard(id) {
    let idx = selected_cards.indexOf(id)

    if (idx === -1) {
        selected_cards.push(id)
        document.getElementById("editCardButton").classList.remove("disabled")
    } else {
        selected_cards.splice(idx, 1)

        if (selected_cards.length === 0) {
            document.getElementById("editCardButton").classList.add("disabled")
        }
    }
}

function batchDeleteCards() {
    let targets = []

    selected_cards.forEach(card => {
        let l_i = card.split("_")
        let list = parseInt(l_i[0])
        let idx = parseInt(l_i[1])
        console.log(list, idx)
        targets.push({
            "target_type": "card",
            "target_id": {
                "target_id_list": list,
                "target_id_card": idx
            }
        })
    })

    let data = {
        "board": currentBoard,
        "owner": boardOwner,
        "targets": targets
    }

    make_modal_request(data, del_board_things_url, "editCardModal", data => {
        insert_html(main_row_id, data)
        document.getElementById("editCardButton").classList.add("disabled")
    })
}

function batchMoveCards() {
    let destination_list = document.getElementById("select_list").value
    let targets = []
    let data = {
        "board": currentBoard,
        "owner": boardOwner,
        "dest_list": destination_list.replace("list_", ""),
        "targets": []
    }

    selected_cards.forEach(card => {
        let l_i = card.split("_")
        let list = parseInt(l_i[0])
        let idx = parseInt(l_i[1])

        console.log(list, idx)
        targets.push({
            "origin_list": list,
            "card_id": idx
        })
    })

    data["targets"] = targets

    make_modal_request(data, move_card_url, "editCardModal", data => {
        insert_html(main_row_id, data)
        document.getElementById("editCardButton").classList.add("disabled")
    })
}

function ok_editCard() {
    let tab_delete = document.querySelector("a[href='#elimina']")
    let tab_sposta = document.querySelector("a[href='#sposta']")

    if (tab_delete.classList.contains('active')) {
        batchDeleteCards()
    } else if (tab_sposta.classList.contains('active')) {
        batchMoveCards()
    }

    selected_cards = []
}