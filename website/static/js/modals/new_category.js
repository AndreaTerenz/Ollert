function ok_newCategory() {
    let name = document.getElementById("categoryName").value;

    make_modal_request({"new_cat_name": name}, new_cat_url, "newCatModal", (data) => {
        console.log(data)
    })

    closeModal("newCatModal")
}