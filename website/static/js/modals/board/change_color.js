function ok_chooseColor() {
    let color = document.getElementById('colorpicker')
    document.body.style.background = color.value

    let request_data = {
        "board_name": currentBoard,
        "edits": [{
            "target_field": "background",
            "new_value": color.value
        }]
    }

    make_modal_request(request_data, edit_board_url, 'chooseColorModal', (data) => {

    })
    closeModal('chooseColorModal')
}