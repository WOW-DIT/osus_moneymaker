document.addEventListener("DOMContentLoaded", (e) => {
    const preLoader = document.getElementById("preloader");
    const checkBoxes = document.querySelectorAll(".form-check-input");

    hideLoader();

    checkBoxes.forEach((element) => {
        element.addEventListener("change", (e) => {
            const sub_name = e.target.getAttribute("data-sub-name")

            toggle_sub_renew(e.target, sub_name)
        })
    })
    

    function toggle_sub_renew(target, sub_name) {
        showLoader();

        const body = {
            sub_name: sub_name
        }
        
        $.ajax({
            url: `/api/method/moneymaker.www.profile_comp.toggle_auto_renew`,
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(body),
            success: function (response) {
                console.log(response.message)
                if(response.message.status == 500) {
                    target.checked = !target.checked
                }
                hideLoader();
            },
            error: function (xhr, status, error) {
                console.log(error);
                hideLoader();
            }
        });

    }


    function hideLoader() {
        preLoader.style.display = "none";
    }

    function showLoader() {
        preLoader.style.display = "inline";
    }

})