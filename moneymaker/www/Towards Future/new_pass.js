

document.addEventListener("DOMContentLoaded", () => {
    const key = getUrlParameter("key");
    const preLoader = document.getElementById("preloader");
    hideLoader();

    const password = document.getElementById("pass");
    const confirmPassword = document.getElementById("cpass");
    const submit = document.getElementById("submit-btn");
    const passError = document.getElementById("pass-error");

    function enableDisableBtn() {
        if (password.value !== confirmPassword.value) {
            passError.classList.remove("hidden");
            confirmPassword.classList.add("error-input")
            submit.classList.add("disable-btn")
            submit.disabled = true
        } else {
            passError.classList.add("hidden");
            confirmPassword.classList.remove("error-input")
            submit.classList.remove("disable-btn")
            submit.disabled = false
        }
    }
    
    password.addEventListener("input", enableDisableBtn);
    confirmPassword.addEventListener("input", enableDisableBtn);

    $("#forget-form").on("submit", function(event) {
        event.preventDefault();

        if(password.value !== confirmPassword.value) {
            alert("كلمة المرور غير متطابقة")
        } else {
            // Reset password
            resetPassword();

        }
    });

    function resetPassword() {
        showLoader();

        $.ajax({
            url: "/api/method/frappe.core.doctype.user.user.update_password",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({
                "new_password": password.value,
                "key": key,
                "logout_all_sessions": 3,
            }),
            success: async function (response) {
                location.href = "login"
            },
            error: function (xhr, status, error) {
                hideLoader();
                alert("انتهت صلاحية هذا الرابط");
            }
        });
    }

    function getUrlParameter(name) {
        const params = new URLSearchParams(window.location.search);
        const value = params.get(name);
        return value;
    }


    function hideLoader() {
        preLoader.style.display = "none";
    }
    
    function showLoader() {
        preLoader.style.display = "inline";
    }
})