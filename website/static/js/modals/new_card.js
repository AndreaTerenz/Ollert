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

    console.log(name, description);
    let clone = template.content.cloneNode(true);
    clone.querySelector(".card-header").textContent = name
    clone.querySelector(".card-body").textContent = truncate(description, 64)
    list.appendChild(clone);

    closeModal("cardModal")
}

// grazie stackoverlow
function truncate(str, n) {
    return (str.length > n) ? str.substr(0, n - 1) + '...' : str;
};