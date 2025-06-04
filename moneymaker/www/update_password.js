

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
            passError.style.display = "inline";
            confirmPassword.classList.add("error-input")
            submit.classList.add("disable-btn")
            submit.disabled = true
        } else {
            passError.style.display = "none";
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
                location.href = "/"
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
    
    function setCookie(name, value, days) {
        let expires = "";
        if (days) {
            const date = new Date();
            date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
            expires = "; expires=" + date.toUTCString();
        }
        document.cookie = name + "=" + value + "; path=/" + expires;
    }
    
    function getCookie(name) {
        const nameEQ = name + "=";
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let c = cookies[i].trim();
            if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
        }
        return null;
    }


    function hideLoader() {
        preLoader.style.display = "none";
    }
    
    function showLoader() {
        preLoader.style.display = "inline";
    }
})