var selected_cards = []

function selectCard(id) {
    console.log(id)
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