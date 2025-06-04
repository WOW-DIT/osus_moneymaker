document.addEventListener("DOMContentLoaded", (e) => {
    const preLoader = document.getElementById("preloader");
    const brandName = document.body.getAttribute("data-brand");
    const logoutBtn = document.getElementById("logout-btn");
    const notiSwitch = document.getElementById("notiSwitch");
    
    logoutBtn.onclick = logout

    hideLoader()

    notiSwitch.addEventListener("change", (e) => {
        toggleNotif();
    })


    function logout() {
        showLoader();
        $.ajax({
            method: 'GET',
            url: '/api/method/logout',
            success: function(response) {
                // Optionally redirect after logout
                window.location.href = `login`;  // or wherever you'd like
            },
            error: function(xhr) {
                hideLoader();
                console.error('Logout failed:', xhr.responseText);
            }
        });
    }

    function toggleNotif() {
        showLoader();
        $.ajax({
            method: 'PUT',
            url: '/api/resources/User/',
            body: JSON.stringify({
                thread_notify: notiSwitch.checked? 1: 0,
            }),
            success: function(response) {
                hideLoader();
            },
            error: function(xhr) {
                hideLoader();
                notiSwitch.checked = !notiSwitch.checked
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