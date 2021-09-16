

function ok_shareModal() {
    let tab_membri = document.querySelector("a[href='#membri']")
    let tab_persone = document.querySelector("a[href='#persone']")
    let tab_link = document.querySelector("a[href='#link']")

    if (tab_membri.classList.contains('active'))
    {

    }
    else if (tab_persone.classList.contains('active'))
    {
        let username = document.getElementById('username').value
        let message = document.getElementById('shareMessage').value
        let permission = document.getElementById('selectAccess').value.toUpperCase()

        console.log(username, message, permission, "AAAAAAAAAAAAAAAAAAa")

        let data = {
            'receiver': username,
            'permissions': permission,
            'board_name': currentBoard,
            'action': 'ADDED'
        }

        console.log(data)

        make_modal_request(data, share_board_url, "shareModal",
            (data) => {
                console.log(data);
            },
            (err) => {
                console.log("AAAAAAAAAAAAAOOOOOOOOOOOOOOOOO")
            }
        )
    }
    else if (tab_link.classList.contains('active'))
    {

    }
}

function getURL() {
    navigator.clipboard.writeText(share_link_url).then(function () {
        alert('Il link è stato copiato con successo!');
    }, function (err) {
        alert('Errore: impossibile copiare link');
    });
}