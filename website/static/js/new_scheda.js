function ok_newScheda() {
    let name = document.getElementById("nomeScheda").value;
    let description = document.getElementById("descrizioneScheda").value;
    let lista = document.getElementById('listaCard');
    let template = document.getElementById('cardTemplate');

    console.log(name, description);
    let clone = template.content.cloneNode(true);
    lista.appendChild(clone);

    closeModal("cardModal")
}
