var selected_cards = []

function selectCard(id) {
    let idx = selected_cards.indexOf(id)

    if (idx === -1) {
        selected_cards.push(id)
        document.getElementById("deleteCardsBtn").classList.remove("disabled")
        document.getElementById("moveCardsBtn").classList.remove("disabled")
    } else {
        selected_cards.splice(idx, 1)

        if (selected_cards.length === 0) {
            document.getElementById("deleteCardsBtn").classList.add("disabled")
            document.getElementById("moveCardsBtn").classList.add("disabled")
        }
    }
}

function batchDeleteCards() {
    //tecnicamente impossibile arrivare qui senza card selezionate ma vabbè
    if (selected_cards.length > 0) {
        let targets = []

        selected_cards.forEach(card => {
            let l_i = card.split("_")
            let list = l_i[0]
            let idx = parseInt(l_i[1])

            targets.push({
                "target_type": "card",
                "target_id": {
                    "target_id_list": list,
                    "target_id_card": idx
                }
            })
        })

        selected_cards.forEach(card =>
            document.getElementById(card).remove())

        let data = {
            "board": currentBoard,
            "targets": targets
        }

        make_modal_request(data, del_board_things_url, "", data => {
            document.getElementById("deleteCardsBtn").classList.add("disabled")
            document.getElementById("moveCardsBtn").classList.add("disabled")
        })
    }
}