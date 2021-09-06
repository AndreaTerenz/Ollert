function ok_shareModal() {
    closeModal("shareModal")
}

function getURL() {
    let text = window.location.href;
    navigator.clipboard.writeText(text).then(function () {
        alert('Il link è stato copiato con successo!');
    }, function (err) {
        alert('Errore: impossibile copiare link');
    });
}