var selected_members = []

function selectMember(id) {
    let name = id.replace("memb_", "")
    let i = selected_members.indexOf(name);
    if (i === -1)
        selected_members.push(name);
    else
        selected_members.splice(i, 1);

    let el = document.getElementById(id)
    el.classList.toggle("selected-member")

    let btn = el.getElementsByTagName("button")[0]
    btn.classList.toggle("btn-success")
    btn.classList.toggle("btn-danger")

    let icon = btn.getElementsByTagName("i")[0]
    icon.classList.toggle("bi-trash")
    icon.classList.toggle("bi-arrow-counterclockwise")

    console.log(selected_members)
}

function ok_shareModal() {
    let tab_membri = document.querySelector("a[href='#membri']")
    let tab_persone = document.querySelector("a[href='#persone']")
    let tab_link = document.querySelector("a[href='#link']")

    if (tab_membri.classList.contains('active')) {
        if (selected_members.length > 0) {
            for (let member of selected_members) {
                let request_data = {
                    "receiver": member,
                    "board_name": currentBoard,
                    "action": "REMOVED"
                }

                make_modal_request(request_data, share_board_url, "", (data) => {
                    console.log("Success?")
                })
            }
        }

        closeModal("shareModal")
    }
    else if (tab_persone.classList.contains('active')) {
        let username = document.getElementById('username').value
        let message = document.getElementById('shareMessage').value
        let permission = document.getElementById('selectAccess').value.toUpperCase()

        let data = {
            'receiver': username,
            'permissions': permission,
            'board_name': currentBoard,
            'action': 'ADDED'
        }

        console.log(data)

        make_modal_request(data, share_board_url, "shareModal", (data) => {
            if (data != null) {
                console.log(data);
            } else {
                console.log("error user not found")
            }
        })
    } else if (tab_link.classList.contains('active')) { }
}

function getURL() {
    let localhost = location.protocol + '//' + location.host;
    navigator.clipboard.writeText(localhost + share_link_url).then(function () {
        alert('Il link è stato copiato con successo!');
    }, function (err) {
        alert('Errore: impossibile copiare link');
    });
}