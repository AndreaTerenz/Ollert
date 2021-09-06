const new_list_btn = document.getElementById("new-list-button")

function ok_newList() {
    let title = document.getElementById("listTitle").value

    if (title) {
        let data = {
            "target_type": "list",
            "target_id": {
                "target_id_board": currentBoard
            },
            "new_data": {
                "list_name": title
            }
        }

        make_modal_request(data, new_list_url, "newListModal", (data) => {
            new_list_btn.insertAdjacentHTML("beforebegin", data)
        })
    }
}