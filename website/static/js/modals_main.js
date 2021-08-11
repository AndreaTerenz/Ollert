function closeModal(id) {
    let mod_el = document.getElementById(id)
    let mod = bootstrap.Modal.getInstance(mod_el)
    mod.hide()
}

function make_modal_request(input_values, url_format, destination) {
    let url = url_format.format(input_values)
    console.log(url)

    fetch(url, {
        method: "POST",
        credentials: 'same-origin',
        headers: {
            "X-CSRFToken": Cookies.get('csrftoken'),
            "X-Requested-With": "XMLHttpRequest"
        },
    }).then((r) => {
        if (r.status === 200) {
            return r.text()
        }
        return null
    }).then((data) => {
        if (data) {
            let dest_el = document.getElementById(destination)
            dest_el.innerHTML = data
        }
    })
}