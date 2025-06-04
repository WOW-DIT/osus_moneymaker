document.addEventListener("DOMContentLoaded", (e) => {
    const openBtn = document.getElementById("open-btn");
    const closedBtn = document.getElementById("closed-btn");
    
    if(!openBtn.classList.contains("active")) {
        openBtn.onclick = showOpen
    }

    if(!closedBtn.classList.contains("active")) {
        closedBtn.onclick = showClosed
    }

    function showOpen() {
        location.href = "support?status=Open"
    }

    function showClosed() {
        location.href = "support?status=Closed"
    }


    function getQueryParam(param) {
        let urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(param);
    }
})