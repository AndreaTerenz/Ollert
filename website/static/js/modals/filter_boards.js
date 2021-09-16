var not_checked = []

function filter_boards(check_id) {
    let to_toggle = []

    let check = document.getElementById(check_id)
    console.log(check.value, check.id, check.checked)
    document.querySelectorAll("li." + check.value).forEach(el => {
        if (!to_toggle.find(e => e === el.id)) {
            to_toggle.push(el.id)
        }
    })

    to_toggle.forEach(el => {
        toggleElement(el)
    })
}

function toggleElement(id_element, keep_hidden = false) {
    let elements = document.getElementById(id_element);

    if (elements.style.getPropertyValue("display") === 'none')
        elements.style.setProperty("display", "flex", "important")
    else
        elements.style.setProperty("display", "none", "important")
}
