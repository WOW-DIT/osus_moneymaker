document.addEventListener("DOMContentLoaded", (e) => {
    const preLoader = document.getElementById("preloader");
    hideLoader();
    
    const email = document.getElementById("email");
    const confirmBtn = document.getElementById("confirm-btn");
    const toEmailBtn = document.getElementById("to-email-btn");

    // toEmailBtn.onclick = goToEmail;
    
    $("#forget-form").on("submit", function(event) {
        event.preventDefault();
        
        requestPasswordRecovery();
    });

    
    
    function requestPasswordRecovery() {
        showLoader();
        $.ajax({
            url: '/api/method/moneymaker.www.forget_pass.reset_password',
            type: 'POST',
            contentType: 'application/json; charset=UTF-8',
            data: JSON.stringify({ email: email.value }),
            success: function(response) {
                console.log(response)

                if(response.message.status == 200) {
                    email.disabled = true
                    confirmBtn.classList.add("hidden");
                    toEmailBtn.classList.remove("hidden");
                } else {
                    alert(response.message.error);
                }
                hideLoader();
            },
            error: function(xhr, status, error) {
                hideLoader();
                alert("Failed to send password recovery email.\nTry again later.");
            }
        });
    }

    function goToEmail() {
        location.href = `mailto:`
    }

    function hideLoader() {
        preLoader.style.display = "none";
    }
    
    function showLoader() {
        preLoader.style.display = "inline";
    }
})