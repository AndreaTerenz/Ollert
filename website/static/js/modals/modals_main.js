function closeModal(id) {
    let mod_el = document.getElementById(id)
    let mod = bootstrap.Modal.getInstance(mod_el)
    mod.hide()
}

//questa funzione permette, dato un certo modale, di aggiungere un listener da eseguire quando esso viene mostrato
//(evento "show.bs.modal")
function addOnShowListener(modalID, listener) {
    //listener è una funzione
    document.getElementById(modalID).addEventListener("show.bs.modal", listener)
}

function insert_html(parent, html) {
    let dest_el = document.getElementById(parent)
    dest_el.innerHTML = html
}

function make_modal_request(input_data, url, modalID, after, on_error = (err)=>{console.log(err)}) {
    fetch(url, {
        method: "POST",
        credentials: 'same-origin',
        headers: {
            "X-CSRFToken": Cookies.get('csrftoken'),
            "X-Requested-With": "XMLHttpRequest"
        },
        body: JSON.stringify(input_data)
    }).then((r) => {
        return {
            "text": r.text(),
            "status": r.status
        }
    }).then((data) => {
        if (data["text"]) {
            after(data)
        }
        else {
            on_error(data["status"])
        }

        if (modalID)
            closeModal(modalID)
    })
}