function ok_chooseColor() {
    let color = document.getElementById('colorpicker')
    document.body.style.background = color.value
    closeModal('closeModal')

    let edits = []
    let request_data = {
        "board_name": currentBoard,
        "edits": []
    }

    edits.push ({
        "target_field": "background",
        "new_value": document.body.style.background = color.value
    })

    request_data["edits"] = edits


}