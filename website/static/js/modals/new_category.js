function ok_newCategory() {
    let name = document.getElementById("categoryName").value;

    if (name !== '') {
        make_modal_request({"new_cat_name": name}, new_cat_url, "newCatModal", (data) => {
            console.log(data)
            insert_html(categories_list_id, data)
        })
    }
    else closeModal("newCatModal")
}