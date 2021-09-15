function ok_chooseColor() {
    let selected_input = document.querySelector(`input[type="radio"]:checked`).value
    console.log(selected_input)

    let color = ""
    if (selected_input === "DEFAULT") {
        color = "#222222"
    }
    else if (selected_input === "CUSTOM") {
        color = document.getElementById('colorpicker')
    }

    let request_data = {
        "board_name": currentBoard,
        "edits": [{
            "target_field": "background",
            "new_value": color.value
        }]
    }

    make_modal_request(request_data, edit_board_url, 'chooseColorModal', (data) => {
        document.body.style.background = color.value
    })
}