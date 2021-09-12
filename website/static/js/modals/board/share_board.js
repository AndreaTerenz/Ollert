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
        let permission = document.getElementById('selectAccess').value

        console.log(username, message, permission)

        let data = {
            'receiver': username,
            'board_name': currentBoard,
            'action': 'ADDED'
        }

        make_modal_request(data, share_board_url, "shareModal", (data) => {
            console.log(data);
        })
    }
    else if (tab_link.classList.contains('active'))
    {

    }

}

function getURL() {
    let text = window.location.href;
    navigator.clipboard.writeText(text).then(function () {
        alert('Il link è stato copiato con successo!');
    }, function (err) {
        alert('Errore: impossibile copiare link');
    });
}